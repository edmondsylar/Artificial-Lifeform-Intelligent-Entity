# The sole purpse of this is to Ensure the later learns How to do it's role better every single time.
# To limit the number of calls being macde to the api, we need to tie this to a pause timeer so that we limit the frequency of contacting the API.

import threading
from rich.console import Console
import time
from flask import Flask, request, jsonify
import os
import google.generativeai as gemini
from dotenv import load_dotenv

# langchain imports
from langchain_google_genai import GoogleGenerativeAI

gemini.configure(api_key=' ')

# api Key
api_key=' '

# declare console
console = Console()

# override the print function with the console print function 
def print(parameter):
    return (console.print(parameter))

# create a log function:
def _sysLog(parameter):
    return (console.log(parameter))


# concisousness class
class Conciousness:
    def __init__(self, layer, layer_instruction):
        
        self.layer_state = False

        # Configure conciousness parameters 
        self.layer = layer
        self.layer_instruction = layer_instruction

        self.top_layer_instruction = None # this is going to be the instruction passed for processing

        # let's register the models responses here.
        self.model_response = None

        self.processed = [] # list of conversations that the model has so far

        #  a list of carefully learned 10 sesson for the day. (list can be empty if system is just fresh)
        self.lessonsToday = []
        
        self.current_best_approch = fr'''        
        '''

        self.change_proposals = []

        # the set current best approach
        self.approach_instruction = fr'''

        This is Your current best Approach. 
        It changes on every 5 change requests, on each response you make esnure to include a change suggestion based on the approach and your continued understanding of your purpose for better output or if you think the Approach is file and there is no needed changes anyway, return "None" for the change suggestions.
        
        # Approach.
        # {self.current_best_approch}.

        # Through the time, the below is a list of the proposed changes to the approach so-far. these will only be made after we have at least 5 change proposals.
        {self.change_proposals}.

        if you feel the need to change the approach, add a single change request in your response.
        # Change request format (Must be json):
        {{
            "change":"your change request"
        }}
        Your system components will autonatically add this to the suggested changes list        

        ''' 

        self.model_prompt = None # this is the only parameter we are going to be passing to the model for processing.
        # the prompt should contain the approach to handle the intructions and any other information model requires. we will 
        # also use a trigger that listens to a change on this variable and calls the model right away.

        # Gemin in Langchain
        self.langLLM = GoogleGenerativeAI(
            model='gemini-pro',
            google_api_key = api_key
        )

        # Defualt gemini Configuration
        self.generation_config = {
                "temperature": 0.2,
                "top_p": 1,
                "top_k": 1,
                "max_output_tokens": 2048,
            }

        # configure gemini model
        self.layer_agent = gemini.GenerativeModel(
            model_name="gemini-pro",
            generation_config=self.generation_config,
        )

        # set the interaction object
        self.gemini_default = self.layer_agent.start_chat()


    # the thinking or the life spark
    def _lifeSpark(self):
        # this function should start a loop to run an "sort of" chain of thought.
        while True:
            if self.layer_state == True:
                prompt_ubild_status = self._build_prompt()
                if prompt_ubild_status == 'completed':
                    _sysLog(self.model_prompt)


    def _build_prompt(self):
        # get all the information available and compose a prompt and return it.
        
        try:
            # gather all information required and create prompt
            prompt = fr'''
            Top Layer request:
            {self.top_layer_instruction}

            # Handling Approach Instructions and notes
            {self.approach_instruction}

            # Environment Info:
            {None}

            # visual Perception (All information from the cameras you can access)
            {None}

            '''
            

            return 'completed'
        except Exception as e:
            return e

    # calling the LLm
    def _LLMCALL(self):
        prompt = self.model_prompt
        # need to pass this to a query length manager function
        
        # check that the system is powered on.
        if self.layer_state == True and self.model_response == None:
            try:
                # default is the LangChain LLM
                response = self.langLLM.invoke(prompt)
                self.model_response = {
                        'status': self.layer_state,
                        'response': response,
                        'used':'Langchain Agent'
                    }
            
            except:
                # use default gemini setup.
                response = self.gemini_default.send_message(prompt)
                self.model_response = {
                        'status': self.layer_state,
                        'response': response,
                        'used': 'Gemini-Pro Default Configuration'
                    }
                            
        else:
            # return 
            return {
                'status' : self.layer_state
            }
    
    # boot the layer by starting the required functions.
    def Boot(self):
        # switch on the layer
        self.layer_state = True
        
        # start the instruction observer loop in a new thread.
        print('starting System....')
        time.sleep(5)
        threading.Thread(target=self._observer_layerLoop).start()
        
        status = self._system_report()
        return status

    # check for system status.
    def _system_report(self):
        # this shares a report to notify about the system's Status.
        return {
            'system_status': self.layer_state,
            'Todays_lessons': self.lessonsToday,
            'Current Approch': self.current_best_approch
        }
    
    
    def _instruction_observer(self):

        # check the value of the prompt
        if self.top_layer_instruction != None:
            print(self.top_layer_instruction + "\n We can no call the model for a request.")
            time.sleep(2)
        else:
            # trigger thought engine
            print('Thinking....')
            time.sleep(2)
            os.system('clear')


    def layer_instruction(self, prompt):
        # register layer command
        self.model_prompt = prompt
        
        # call the model Query function
        threading.Thread(target=self._LLMCALL).start()

        pass        

    
    def _observer_layerLoop(self):
        # we are are going to loop over the instruction obsserver to trigger the thought process.
        while True: # check is the layer is active
            if self.layer_state == True:
                # run the observer
                self._instruction_observer()
                continue
            else:
                return {
                    'msg':'Layer status is registered as OFF (False)',
                    'Layer State' : self.layer_state
                }
            
        return False
            
    # system shutdown function
    def _systemShutdown(self):
        # turn off layer
        self.layer_state = False
        print('Shuting Down system in 5 seconds....')

        # wait for 5 seconds 
        time.sleep(5)
        return False #return system


timer = 0
_layer = 'AgentModelLayer'
_instruction= 'Not Yet share any instructions'

# test the class
_concisousNess = Conciousness(layer=_layer, layer_instruction=_instruction)

# create flask app.
app = Flask(__name__)

# default entry
@app.route('/')
def _entry():
    # This is the entry of the conciousness.
    status = _concisousNess._system_report()

    return {
        'Layer State': status
    }

# shutdown the system
@app.route('/shutdown')
def _shutdown():
    # send shutdown command.
    _concisousNess._systemShutdown()
    status = _concisousNess._system_report()
    return {
        'status': status
    }


@app.route('/test', methods=['POST'])
def _test():
    # lest the LLM output
    data = request.get_json()

    output = _concisousNess._LLMCALL(fr'{data}')
    return(output)


# start System.
@app.route('/start', methods=['POST'])
def _startSystem():

    data = request.get_json()

    print(data)

    # start the system.
    status = _.Boot()

    return {
        'status': status
    }


# start the layer api
if __name__ == '__main__':
    app.run(debug=True, port=5031)