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
        self.system_diagnosis = None # this will hold the diagnosis of the system.
        self.keyboards_inputs = None # this will hold the keyboard inputs of the system.
        self.thoughts = 'System is free, continue exploring the world as you wish by thinking and learning as you wait for the next interaction' # this is going to be a string that represents the thoughts of the system.
        
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
        try:
            # convert msg to dict 
            msg = json.loads(layer_msgs['message'])
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


    def initiateThought(self):

        prompt = self._build_prompt()        
        console.log(prompt)

        # clear the user input and speech to text. after processing.                
        # let's call the aspirational layer.
        layer_one_response = self._call_layer(self.layer1, self._build_prompt())
        # console.log(layer_one_response)

        console.log(type(layer_one_response), layer_one_response)
        
        if layer_one_response['message']:
            # in a thread we are going to call the _build_thoughts function.
            threading.Thread(target=self._build_thoughts, args=(layer_one_response['message'],)).start()

            # we are goingt o call later 2.
            layer_two_response = self._call_layer(self.layer2, layer_one_response['message'])
            console.log(type(layer_two_response) ,layer_two_response)

            # input('Enter to continue')
            if (layer_two_response['message']):
                msgs = self.extract_messages(layer_two_response)

                # in a thread we are going to call the _build_thoughts function.
                threading.Thread(target=self._build_thoughts, args=(layer_one_response['message'],)).start()

                # call layer 3.
                layer_three_response = self._call_layer(self.layer3, fr"{prompt} \n\n {msgs['NORTH']}")
                console.log(layer_three_response)

                if (layer_three_response['message']):
                    msgs = self.extract_messages(layer_three_response)
                    # in a thread we are going to call the _build_thoughts function.
                    threading.Thread(target=self._build_thoughts, args=(layer_one_response['message'],)).start()

                    # call layer 4.
                    layer_four_response = self._call_layer(self.layer4, fr"{prompt} \n\n {msgs['NORTH']}")
                    console.log(layer_four_response)

                    if (layer_four_response['message']):
                        # msgs = self.extract_messages(layer_four_response)
                        # in a thread we are going to call the _build_thoughts function.
                        threading.Thread(target=self._build_thoughts, args=(layer_one_response['message'],)).start()

                        # call layer 5.
                        layer_five_response = self._call_layer(self.layer5, fr"{prompt} \n\n Strictly Focus on the North Bound Messages: {layer_one_response['message']}")
                        console.log(layer_five_response)

                        # we are going to call the final layer.
                        if (layer_five_response['message']):
                            msgs = self.extract_messages(layer_five_response)

                            # in a thread we are going to call the _build_thoughts function.
                            threading.Thread(target=self._build_thoughts, args=(layer_one_response['message'],)).start()

                            layer_six_response = self._call_layer(self.layer6, fr"{prompt} \n\n {msgs['NORTH']}")
                            console.log(layer_six_response)

                            # this layer is going to retriggr the whole process by recalling the initiateThought function.
                            if (layer_six_response['message']):
                                # clear the keyboard inputs.
                                self.keyboards_inputs = None
                                # clear the audio inputs.
                                self.audio_inputs = None

                                self.initiateThought()

        

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
        {self.keyboards_inputs}

        # system diagnosis. (The computer stats and diagnosis of the system you are running on)
        {self.system_diagnosis}

        # Internal Self Awarness
        {self.selfAwareness}


        #system configuration.
        This is your current system configuration. by which you run. Refer to this for personal adjustments.
        {self.system_configuration}

        """
        
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

        console.log('received audio input and awaiting command for execution....')
        

    def _visual_receiver(self, vtt):
        self.visual_inputs = vtt
        

    def _keyboard_receiver(self, user_input):
        self.keyboards_inputs = user_input

        console.log('waiting for 3 seconds...')
        # this input will call the initiateThought function.
        self.initiateThought()
        
        

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