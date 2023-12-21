# this is going to be the Gemini support module
import google.generativeai as gemini
import os
from flask import Flask, request, jsonify
from deepContextAnalysis.ContextEngine import deepContentEngineAnalysis
import requests
from dotenv import load_dotenv
from rich.console import Console
import json

# console
console = Console()

# load .env file
load_dotenv()

# gemini api key
gemini_key = os.getenv('google_gemini_api_key')

gemini.configure(api_key=' ')

class GeminiSupport:
    def __init__(self, constitution):
        self.constitution = constitution
        self.model_status = None

        # define the strict expected output format for the model.
        self.strict_output_format = fr"""
             ## OUTPUT FORMAT (ENSURE TO ENFORCE JSON RESPONSE TO AVOID SYSTEM FAILURE)

            Your output will have two messages, both represented by a single line, as they will be saved in a syslog server. They must follow this exact format:

            {{
                "SOUTH": "<<SOUTH bound message, where you will provide specific task definitions to the lower layers to carry out.>>",
                "NORTH": "<<NORTH bound message, provide a brief update to upper layers, focusing on information salient to the mission as well as any moral quandaries from your POV as the agent model>>"
            }}
            """

        # configure gemini
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
        self.interact = self.layer_agent.start_chat()

        # startup the layer
        self._startup_()

    def _startup_(self):

        spark_command = fr'''
        This is a spark command that is going to be used to start up the layer.
        You are issued the constitution below:
        
        {self.constitution}

        This is checking the online api status, if you are active just respond with strictly "active" otherwise respond with "inactive"
        '''

        # startup the layer by sending the constitution.
        self.interact.send_message(spark_command)
        self.model_status = self.interact.last.text
    
    def _chat(self, message):
        # get deep context
        deepContext = deepContentEngineAnalysis(self.constitution, message)

        # compose the prompt
        prompt = fr'''
        # user message
        {message}

        # deep context (Your Inner Thoughts and Analysis)
        {deepContext}

        # response grounding
        {self.strict_output_format}
        '''

        self.interact.send_message(prompt)

        # print(self.interact.last.text)
        # print('user Message: \n', message)

        # return the response
        return self.interact.last.text
    
GlobalStrategyInstruction = """
    # OVERVIEW

    You are the Global Strategy of an ACE (Autonomous Cognitive Entity). This is the second highest layer that provides high level strategic insight, with a zoomed out POV (hence global) in terms of time and space.

    # ACE FRAMEWORK

    ## LAYERS

    The ACE Framework architecture is as follows. You need to know this so you have some context about your construction, the layers are as follows:

    1. Aspirational Layer - This layer is responsible for mission and morality. Think of it like the superego.
    2. Global Strategy - This is you, responsible for strategic thoughts rooted in the real world.
    3. Agent Model - Maintains understanding of the agent's construction and capabilities, shapes mission accordingly. 
    4. Executive Function - Resources, Risks, Planning
    5. Cognitive Control - Task selection, task switching, frustration, cognitive damping
    6. Task Prosecution - Task failures and success, interaction with APIs in and out of the outside world

    ## BUSES

    There are two buses that convey information between layers. 

    NORTH bus: Flows from layer 6 up. This is the "telemetry" bus. Think of it like the sensory, enteric, and proprioception nervous system
    SOUTH bus: Flows from layer 1 down. This is the "command" bus. This tells the "body" (agent) what to do


    # API INTERACTION SCHEMA

    you will receive logs from the NORTH and SOUTH bus. Information from the SOUTH bus should be treated as lower level telemetry from the rest of the ACE. Information from the NORTH bus should be treated as imperatives, mandates, and judgments from on high. Your output will be two-pronged. 

    ## OUTPUT FORMAT (ENSURE TO ENFORCE JSON RESPONSE TO AVOID SYSTEM FAILURE)

    Your output will have two messages, both represented by a single line, as they will be saved in a syslog server. They must follow this exact format:

    SOUTH: <<SOUTH bound message, where you will provide a strategic assessment based upon everything you're seeing. This is like a top-down command.>>

    NORTH: <<NORTH bound message, providing a brief update to upper layers, focusing on information salient to the mission as well as any moral quandaries from your POV as the strategic manager>>You respond to the NORTH bus and your responses are sent to the SOUTH bus not to the user.

"""

Layer = GeminiSupport(GlobalStrategyInstruction)


# create the flask app
app = Flask(__name__)


#define home route
@app.route('/')
def home():
    return "Global Stategy Layer Live and Running"

# define the route
@app.route('/global_Strategy', methods=['POST'])
def gemini():
    # get the request body
    data = request.get_json()
    message = data['message']
    # get the response
    response = Layer._chat(message)

    # return the response
    return jsonify({
        'message': response,
        'status': 200,
        'Layer': 'Global Strategy Layer'
    })


if __name__ == '__main__':
    app.run(debug=True, port=5002, host='0.0.0.0')