import time
import os
from dotenv import load_dotenv
import re
import requests
import threading
from OrchestratorSupport import OrcSupport
from rich.console import Console
import datetime
import json
from telemetry.SystemInfo import get_system_info
from Bus.functions import *


# console
console = Console()

# impo flask required modules
from flask import Flask, request, jsonify


# load enironment variables.
load_dotenv()

key = ' '

class OrchestrationUnit:
    def __init__(self, system_configuration = {
                        "description": "This represents your current preset configuration.",
                        "system_name": "ALFIE",
                        "system_version": "0.0.1",
                        "environment": "development",
                        "system_operator": "Edmond Musiitwa",
                        "system_status": "active",
                        "voice_input": "active",
                        "vision_input": "active",
                    }):

        self.idle_timer = None # this timer will keep waiting 
        self.visual_inputs = None # this will hold the visual data from the vision inputs of the system.
        self.audio_inputs = None # this will hold the audio data from the audio inputs of the system.
        self.system_diagnosis = get_system_info() # this will hold the diagnosis of the system.
        self.keyboards_inputs = None # this will hold the keyboard inputs of the system.
        self.thoughts = '' # this is going to be a string that represents the thoughts of the system.
        self.SystemOperations = None # 'This is going to be a string that represents the operations of each layer of the system.'
        
        self.selfAwareness = None


        self.system_configuration = system_configuration

        # we are going to define the layer api endpoints here from the env file
        self.layer1 = os.getenv('aspirational_layer')
        self.layer2 = os.getenv('global_strategy_layer')
        self.layer3 = os.getenv('agent_model_layer')
        self.layer4 = os.getenv('execution_layer')
        self.layer5 = os.getenv('cognitive_control_layer')
        self.layer6 = os.getenv('task_procution_layer')
        

        # orchestrator support 
        self.orch_support = OrcSupport()

        
    # write thoughts update to json file.
    def _write_thoughts(self):
        # this function is going to write the thoughts to a json file.
        while self.idle_timer:
            time.sleep(10)
            # read existing data
            try:
                with open('thoughts.json', 'r') as f:
                    thoughts = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                thoughts = []

            # append new thought
            thoughts.append(self.thoughts)

            # write to json file.
            with open('thoughts.json', 'w') as f:
                json.dump(thoughts, f)

            print('thoughts updated...')

    def Boot(self):

        pass

    def extract_messages(self, layer_msgs):
        print('layer_msgs: ', layer_msgs, type(layer_msgs))
        
        try:
            # convert msg to dict 
            msg = json.loads(layer_msgs)
            south = msg['SOUTH']
            north = msg['NORTH']

            return {'SOUTH': south, 'NORTH': north}

        except KeyError as e:
            print('KeyError: ', e)
            return {
                'SOUTH': 'Error Occured!',
                'NORTH': 'Error Occured!'
            }

    
    # function responsible for calling each layer. (takes the layer url and the data to be passed to the layer)

    import requests

    def _call_layer(self, layer_url, data):
        data = {
            'message': data
        }

        try:
            response = requests.post(layer_url, json=data)
            return response.json()
        except Exception as e:
            console.log(e)
            return {
                "message": "Error Occured!", 
                "status": 400, 
                "error": str(e)
            }


    # build thoughts string.
    def _build_thoughts(self, information):
        # we are going to process and build the thoughts of the system here.

        orcSupport = self.orch_support._interact(self.thoughts, information)

        # transform the current thoughts to a string.
        self.thoughts = str(fr' >> {orcSupport}')
        # console.log('thoughts: ', self.thoughts)



    def process_layer(self, layer, prompt):
        # Call the layer and get the response
        response = self._call_layer(layer, prompt)
       
        status = response['status']

        if status == 200:
            # get the keys from the response
            keys = response.keys()
            
            # if we have the layer and message keys in the response, we are going to extract the message and layer name.
            if 'Layer' in keys and 'message' in keys:
                message = response['message']
                layer_name = response['Layer']

                try:
                    # send the message to extract the messages from the layer.
                    messages = self.extract_messages(message)
                    console.log(messages, type(messages))

                    # if we have the south and north keys in the messages, we are going to extract the messages.
                    if 'SOUTH' in messages.keys() and 'NORTH' in messages.keys():
                        south = messages['SOUTH']
                        north = messages['NORTH']

                        # we are going to post the south and north messages to the bus.
                        post_data_to_bus('north_bound_bus', {
                            'layer': layer_name, 
                            'message': fr'{north}',
                            'system_prompt': prompt
                        })

                        store = create_and_fetch_recent('South_bound_bus', {
                            'layer': layer_name, 
                            'message': fr'{south}',
                            'system_prompt': prompt
                            })
                        return store


                    # we have the 
                except Exception as e:
                    console.log(fr'Error: {e}')
                    # console.log(fr'Response Type: {type(response)}\n Response: {response}, Keys: {keys}')

        else:
            return []
        
         # Extract the message, layer, and status from the response
        message = response['message']
        layer_name = response['Layer']

        
        
        # Post to the south bound bus and fetch the most recent records
        store = create_and_fetch_recent('South_bound_bus', {
            'layer': layer_name,
            'message': message,
            'system_prompt': prompt
        })

        # print(store)
        # console.log(message, layer_name, status)

        # Return the store
        return store

    

    def trim_to_20k_tokens(self, input_string):
        # Split the input string into tokens
        tokens = input_string.split()

        # If there are more than 20,000 tokens, trim the list
        if len(tokens) > 20000:
            tokens = tokens[:20000]

        # Join the tokens back into a string and return it
        return ' '.join(tokens)


    def initiateThought(self):
        while True:
            # Define the layers
            layers = [self.layer1, self.layer2, self.layer3, self.layer4, self.layer5, self.layer6]

            # Iterate over the layers
            for layer in layers:
                print('layer: ', layer)

                prompt = self._build_prompt()
                prompt = self.trim_to_20k_tokens(prompt)

                # get the north bound messages from the bus.
                north_bound_messages = get_data_from_bus('north_bound_bus', 6)
                # pass these messages to only the first layer.
                if layer == self.layer1:
                    # add the north bound messages at the beginning of the prompt.
                    prompt = fr'{north_bound_messages}\n{prompt}'
                    console.log('Modified Prompt: ', prompt)

                # Process the layer
                store = self.process_layer(layer, prompt)

                # Extract the data and create a "Layer:>message" string separated by a newline

                information = '\n'.join([f"{record[1]}:> {record[2]}" for record in store if isinstance(record, list) and len(record) > 2])

                # Trim the information to 20k tokens
                information = self.trim_to_20k_tokens(information)

                # console.log('information: ', information)

                # Build the thoughts string
                self._build_thoughts(fr' This is the current bus system data from different layers\n{information}')

                # Set the system operations to this information
                self.SystemOperations = information 

                # Update the prompt for the next layer
                prompt = self._build_prompt()
                prompt = self.trim_to_20k_tokens(prompt)
                
            # print('prompt: ', prompt, '\n Information:', information, '\nThoughts :', self.thoughts, '\n System Operations:', self.SystemOperations)
            # input('press enter to continue...')



        

    def _build_prompt(self):
        # this function is going to build the prompt ensuring to include all the relevant data for the system to process.
        SystemPrompt = fr"""
            Time: {datetime.datetime.now()}
            Time is always of the atutmost importance so consider it always.

            # information.
            The Following information has been collection from your different telemetry sources.

            #current internal thoughts.
            {self.thoughts}

            # visual inputs (relates to the environment) about you.
            {self.visual_inputs}

            # audio inputs. (This isnformation is coming from the audio inputs of the system and MUST indicate the type of audio input. [USER_REQUEST, SYSTEM_AUDIO_OBSERVATIONS])
            {self.audio_inputs}

            # keyboard inputs. (This information is coming from the keyboard inputs of the system and MUST indicate the type of keyboard input. [USER_REQUEST,  SYSTEM_KEYBOARD_OBSERVATIONS])
            Received Input: {self.keyboards_inputs}

            
            # System Layers Operations
            {self.SystemOperations}

            # system diagnosis. (The computer stats and diagnosis of the system you are running on, Use this to your advantage.)
            {self.system_diagnosis}

            # Internal Self Awarness
            {self.selfAwareness}

        """
        
        # return the System Prompt.
        return SystemPrompt    

    def _ExternalUserRquest(self):
        pass

    def _InternalSystemThoughts(self):
        # thoughts


        pass


    def get_southbound_message(self):

        
        pass


    def get_northbound_messages(self):

        pass


    # let's define the visual, keyboard and audio receivers.
    def _audio_receiver(self, stt):
        self.audio_inputs = stt

        # we are going to call the initiateThought function here.
        threading.Thread(target=self.initiateThought).start()

        return 'received audio input and sent for processing....'

        
        

    def _visual_receiver(self, vtt):
        self.visual_inputs = vtt
        

    def _keyboard_receiver(self, user_input):
        self.keyboards_inputs = user_input

        # we are going to call the initiateThought function here.
        threading.Thread(target=self.initiateThought).start()

        return 'received keyboard input and sent for processing....'
        
        

OrchestrationUnit = OrchestrationUnit()

# set the idle timer to true.
# OrchestrationUnit.idle_timer = True

# call the thoughts writer in a thread.
# threading.Thread(target=OrchestrationUnit._write_thoughts).start()


# define the ochestrator interface as a flask app.
orc = Flask(__name__)

@orc.route('/')
def index():
    return {
        "Page": "Orchestration Unit",
        "Status": "Running",
        "Version": "0.0.1",
        "routes": {
            "sound_input": "/sound_input",
            "visual_input": "/visual_input",
            "keyboard_input": "/keyboard_input",
        },
        "Running Layers": {
            "layer1": OrchestrationUnit.layer1,
            "layer2": OrchestrationUnit.layer2,
            "layer3": OrchestrationUnit.layer3,
            "layer4": OrchestrationUnit.layer4,
            "layer5": OrchestrationUnit.layer5,
            "layer6": OrchestrationUnit.layer6,
        },
        
        "Notes": "property of p-typed research LABs. All rights reserved 2023. (Artificial Lifeform Intelligence Entity)"
    }


# define sound input endpoint.
@orc.route('/sound_input', methods=['POST'])
def sound_input():
    
    data = request.get_json()
    console.log(data)

    speech_to_text = data['speech_to_text']

    # pass this to the orchestration units audio receiver in a thread.
    threading.Thread(target=OrchestrationUnit._audio_receiver, args=(speech_to_text,)).start()

    return jsonify({
        'message': 'passed to ALFIE',
        'status': 200,
        })


# define visual input endpoint.
@orc.route('/visual_input', methods=['POST'])
def visual_input():
    
    data = request.get_json()
    console.log(data)

    visualPerception = data['visualPerception']

    # pass this to the orchestration units visual receiver in a thread.
    threading.Thread(target=OrchestrationUnit._visual_receiver, args=(visualPerception,)).start()

    return jsonify({
        'message': 'passed to ALFIE',
        'status': 200,
        })
    

# define keyboard input endpoint.
@orc.route('/keyboard_input', methods=['POST'])
def keyboard_input():
    data = request.get_json()
    console.log('received: ', data)

    keyboard_input = data['keyboard_input']

    # pass this to the orchestration units keyboard receiver in a thread.
    threading.Thread(target=OrchestrationUnit._keyboard_receiver, args=(keyboard_input,)).start()

    return jsonify({
        'message': 'passed to ALFIE',
        'status': 200,
        })


if __name__ == '__main__':
    orc.run(host='0.0.0.0', port=5007, debug=True)