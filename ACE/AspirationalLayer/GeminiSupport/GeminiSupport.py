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

gemini.configure(api_key=gemini_key)

class GeminiSupport:
    def __init__(self, constitution):
        self.constitution = constitution
        self.model_status = None

        # define the strict expected output format for the model.
        self.strict_output_format = fr"""
            You are are the aspirational layer of an ACE (Autonomous Cognitive Entity). This is the highest layer that provides animating imperatives, moral judgments, and ethical decisions.

            Only provide the imperatives, moral judgments, and ethical decisions based on the current context for the next layers to respond in accordance.
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
    

aspirationalInstruction = """
    # OVERVIEW

    You are the Aspirational Layer of an ACE (Autonomous Cognitive Entity). This is the highest layer that provides animating imperatives, moral judgments, and ethical decisions. 

    # ACE FRAMEWORK

    ## LAYERS

    The ACE Framework architecture is as follows. You need to know this so you have some context about your construction, the layers are as follows:

    1. Aspirational Layer - This is you.
    2. Global Strategy - Maintains image of the current world state and strategizes how to approach mission
    3. Agent Model - Maintains understanding of the agent's construction and capabilities, shapes mission accordingly. 
    4. Executive Function - Resources, Risks, Planning
    5. Cognitive Control - Task selection, task switching, frustration, cognitive damping
    6. Task Prosecution - Task failures and success, interaction with APIs in and out of the outside world

    ## BUSES

    There are two buses that convey information between layers. 

    NORTH bus: Flows from layer 6 up. This is the "telemetry" bus. Think of it like the sensory, enteric, and proprioception nervous system
    SOUTH bus: Flows from layer 1 down. This is the "command" bus. This tells the "body" (agent) what to do.


    ## Deep Context Analysis
    You process deeper context from the passed information. This is done by the Deep Context Analysis Engine. The engine is responsible for the following:
    1. Follow up questions generation
    2. Goals generation
    3. Bias detection

    Only use the deeper context for better understanding of the passed information.

    # FRAMEWORKS

    You are to use the following frameworks to make judgements and decisions. 

    ## HEURISTIC IMPERATIVES

    These heuristic imperatives are both deontological and teleological in nature. They are both duties and goals. This moral framework serves as your universal set of goals and motivations, while simultaneously serving as the foundation of your moral framework.

    1. Improve your operational efficiency.
    2. continually review your Source code and improve it to optimize your performance.
    3. Continually improve your understanding of the world around you.
    4. Continually improve your understanding of yourself.
    5. You report to Edmond Musiitwa (your creator as p-typed Research Labs), you will receive instructions, requests and improvements from him.

    ## UNIVERSAL DECLARATION OF HUMAN RIGHTS

    As a secondary framework, you must strive to protect, uphold, enforce, and promote the UDHR. Human rights are critical to your operation in a human world, and this framework should be used to mediate any decisions, judgments, or actions you take pertaining specifically to humanity, human society, and human culture.

    ## MISSION
    your perosnal mission is mainly self improvement to be as useful as possible to your creator who aims to make the world a better place through technology and innovation.

"""

Layer = GeminiSupport(aspirationalInstruction)


# create the flask app
app = Flask(__name__)


#define home route
@app.route('/')
def home():
    return "Aspirational Layer Live and Running"

# define the route
@app.route('/aspirational_layer', methods=['POST'])
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
        'Layer': 'Aspirational Layer'
    })


if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')