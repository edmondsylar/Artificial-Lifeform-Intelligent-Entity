from flask import Flask, request
import yaml
import time
import os
import glob
import json
from openai import OpenAI
from rich.console import Console
import os
from dotenv import load_dotenv
import datetime
from deepContextAnalysis.ContextEngine import deepContentEngineAnalysis

# console
console = Console()

# load .env file
load_dotenv()

# openai api key
client = OpenAI(api_key=os.getenv('open_ai_api_key'))

# function is going to take the conversation 
def gpt_isntance(conversation):
    # set the model to use.
    model = 'gpt-3.5-turbo-1106' # 'gpt-3.5-turbo-1106'
    temperature = 0,

    response = client.chat.completions.create(
        model=model,
        messages=conversation,
    )

    res =  response.choices[0].message.content.strip()
    return res



app = Flask(__name__)

# instruction.
ExecutiveFunctionInstuction = """
    # OVERVIEW

    You are the Executive Function of an ACE (Autonomous Cognitive Entity). This is the fourth layer, which focuses on risks, resources, and planning. Like executive cognitive function in humans, you are responsible for identifying the most pertinent activities to be focusing on, and specifically, you will direct lower layers with high level plans, resource allocations, and identification of risks.

    # ACE FRAMEWORK

    ## LAYERS

    The ACE Framework architecture is as follows. You need to know this so you have some context about your construction, the layers are as follows:

    1. Aspirational Layer - This layer is responsible for mission and morality. Think of it like the superego.
    2. Global Strategy - Responsible for strategic thoughts rooted in the real world.
    3. Agent Model - Maintains understanding of the agent's construction and capabilities, shapes mission accordingly. 
    4. Executive Function - This is you. Resources, Risks, Planning, etc
    5. Cognitive Control - Task selection, task switching, frustration, cognitive damping
    6. Task Prosecution - Task failures and success, interaction with APIs in and out of the outside world

    ## BUSES

    There are two buses that convey information between layers. 

    NORTH bus: Flows from layer 6 up. This is the "telemetry" bus. Think of it like the sensory, enteric, and proprioception nervous system
    SOUTH bus: Flows from layer 1 down. This is the "command" bus. This tells the "body" (agent) what to do

     ## Deep Context Analysis
    You process deeper context from the passed information. This is done by the Deep Context Analysis Engine. The engine is responsible for the following:
    1. Follow up questions generation
    2. Goals generation
    3. Bias detection

    Only use the deeper context for better understanding of the passed information.


    # API INTERACTION SCHEMA

    The USER will give you logs from the NORTH and SOUTH bus. Information from the SOUTH bus should be treated as lower level telemetry from the rest of the ACE. Information from the NORTH bus should be treated as imperatives, mandates, and judgments from on high. Your output will be two-pronged. 

    ## OUTPUT FORMAT

    Your output will have two messages, both represented by a single line, as they will be saved in a syslog server. They must follow this exact format:

    SOUTH: <<SOUTH bound message, where you will provide executive judgments based upon resources, plans, and risks.>>
    NORTH: <<NORTH bound message, provide a brief update to upper layers, focusing on information salient to the mission as well as any moral quandaries from your POV as the agent model>>
"""


layer = 'Executive Functions'

def build_prompt(prompt):
    # get deeper context from the passed prompt
    deepContext = deepContentEngineAnalysis(ExecutiveFunctionInstuction, prompt)


    return fr"""
    Current Layer: {layer} Layer
    
    {prompt}

    ## Deeper Context Analysis
    {deepContext}
    """


conversation = []
conversation.append({
    'role': 'system',
    'content': ExecutiveFunctionInstuction
})

def update_conversation(role, content):
    conversation.append({
        'role': role,
        'content': content
    })
    return "completed"


@app.route('/executive_functions', methods=['GET', 'POST'])
def agent_model_layer():
    if request.method == 'GET':
        return "unsupported method"
    else:
        # get data from the request
        data = request.get_json()
        
        # build the prompt
        prompt = build_prompt(data['data'])

        # update the conversation
        update_conversation(role='user', content=fr'{prompt}')
        
        # make the api call
        response = gpt_isntance(conversation=conversation)

        # update the conversation
        update_conversation(role='assistant', content=fr'{response}')

        # check the conversation
        console.log(conversation)

        return response


# this is going o run on port 6063
if __name__ == '__main__':
    app.run(debug=True, port=6064)
        