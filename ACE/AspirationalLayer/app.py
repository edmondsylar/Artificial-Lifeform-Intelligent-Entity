from flask import Flask, request
from ace_support import *
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
import layerdb as ldb
import threading

# import the configurable layer.
from configurableLayer import ConfigurableLayer

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
    response = client.chat.completions.create(
        model=model,
        messages=conversation,
    )

    res =  response.choices[0].message.content.strip()
    return res



app = Flask(__name__)

# instruction.
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

layer = 'Aspirational Layer'
database = "aspirationalLayer.db"

def build_prompt(prompt):
    deepContext = deepContentEngineAnalysis(aspirationalInstruction, prompt)

    return f"""
    Current Layer: {layer} Layer
    
    {prompt}

    ## Deeper Context Analysis
    {deepContext}
    """



conversation = []
# inialize db and create tables
conn = ldb.layerDBManager(database)
conn.init_db()
conn.close() 

def clean_conversation():
    conn = ldb.layerDBManager(database)
    temp_conv  = conn.select('conversation', ['*'])
    conn.close()

    # convert the messages to a list of dictionaries
    for each in temp_conv:
        conversation.append({
            'role': each[1],
            'content': each[2]
        })

    try:
        deducted = [conversation[0]] + conversation[-4:]
        return deducted
    except:
        return conversation

# check for first time run
convLen = len(clean_conversation())

if (len(clean_conversation()) <= 0):
    conn = ldb.layerDBManager(database)
    conn._firstRun()
    conn.close()


@app.route('/aspirational_layer', methods=['GET', 'POST'])
def aspirational_layer():
    if request.method == 'GET':
        return "unsupported method"
    else:
        # get data from the request
        data = request.get_json()
        # build the prompt
        prompt = build_prompt(data['data'])

        # update the conversation in the database
        conn = ldb.layerDBManager(database)
        conn.insert('conversation', ['role', 'content'], ['user', fr'{prompt}'])
        conn.close()
        
        # get the conversation
        conversation = clean_conversation()

        # make the api call
        response = gpt_isntance(conversation=conversation)

        # update the conversation in the database
        conn = ldb.layerDBManager(database)
        conn.insert('conversation', ['role', 'content'], ['assistant', fr'{response}'])
        conn.close()
        
        # post to the south bound bus and call the next layer
        data = {
            'layer': 'Aspirational Layer',
            'messages': response
        }

        # post to the south bound bus and call the next layer
        post_southbound_bus_message(data)

        # post to the south bound bus and call the next layer
        post_northbound_bus_message(data)

        print('Posted to the south bound bus')

        threading.Thread(target=nxtLayer, args=('globalStrategy',)).start()

        console.log(f'[bold green]Aspirational Layer[/bold green]: {response}')
        return response


@app.route('/aspirational_layer_v2', method=['GET', 'POST'])
def aspirational_layer_v2():
    layerAgent  = ConfigurableLayer(aspirationalInstruction) #invoke the configurable layer.

    layerAgent.add_situation('''
    System Situation.
                             
    ''')


    pass


# this is going o run on port 6063
if __name__ == '__main__':
    app.run(debug=True, port=6061)
        