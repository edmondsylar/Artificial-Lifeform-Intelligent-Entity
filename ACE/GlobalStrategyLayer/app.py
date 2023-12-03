from flask import Flask, request
import yaml
import time
import os
from ace_support import *
from openai import OpenAI
from rich.console import Console
import os
from dotenv import load_dotenv
import threading
from deepContextAnalysis.ContextEngine import deepContentEngineAnalysis
import layerdb as ldb


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

    ## OUTPUT FORMAT

    Your output will have two messages, both represented by a single line, as they will be saved in a syslog server. They must follow this exact format:

    SOUTH: <<SOUTH bound message, where you will provide a strategic assessment based upon everything you're seeing. This is like a top-down command.>>

    NORTH: <<NORTH bound message, providing a brief update to upper layers, focusing on information salient to the mission as well as any moral quandaries from your POV as the strategic manager>>You respond to the NORTH bus and your responses are sent to the SOUTH bus not to the user.

"""

layer = 'Global Strategy'
database = 'GlobalStrategyLayer.db'



def build_prompt(prompt):
    # get deeper context from the passed prompt
    deepContext = deepContentEngineAnalysis(GlobalStrategyInstruction, prompt)


    return fr"""
    Current Layer: {layer} Layer
    
    {prompt}

    ## You Deeper Context Analysis
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



@app.route('/global_strategy_layer', methods=['GET', 'POST'])
def agent_model_layer():
    if request.method == 'GET':
            return "unsupported method"
    else:
        # get data from the request
        data = request.get_json()
        
        print("received at Global", data)

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

        # we are goning to start layer 2 here by passing the recent posting to the South bound bus.

        # return the response

        parts = response.split("\n\n")

        south = parts[0].replace("SOUTH: ", "")
        north = parts[1].replace("NORTH: ", "")

        # post to the south bound bus and call the next layer
        data = {
            'layer': 'Global Strategy Layer',
            'messages': south
        }
        post_southbound_bus_message(data)

        # post to the north bound bus and call the next layer
        data = {
            'layer': 'Global Strategy Layer',
            'messages': north
        }
        post_northbound_bus_message(data)

        # call the next layer in a new thread.
        threading.Thread(target=nxtLayer, args=('agentModel',)).start()

        console.print(f"[bold green]Global Strategy Layer[/bold green] says: {response}")

        return response


# this is going o run on port 6063
if __name__ == '__main__':
    app.run(debug=True, port=6062)
        