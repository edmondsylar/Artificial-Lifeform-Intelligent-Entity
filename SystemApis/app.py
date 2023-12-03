# thi api is going to server as the bus for the ACE framework.
# the bus is going to have extra functions to handle other data related tasks except the data flow btw the layers.
from flask import Flask, render_template, request, jsonify
from BridgeController import get_conversation, insert_conversation
from flask import g
from database import DatabaseManager
from busControl import _interact
import threading
import layerdb as ldb
from ace_support import *

import sqlite3
import os


# Create Flask application instance
app = Flask(__name__)


# configure the database
conn = ldb.layerDBManager('bus.db')
conn.init_bus_database()
conn.close() 


# Define a route and its corresponding function
@app.route('/')
def home():
    return "Server is up and running!"


# define route to get the messages of a given layer from the conversation table.
@app.route('/conversation_get', methods=['GET'])
def conversation_get():
    systedb = DatabaseManager('bus.db')
    conversation = []

    # get messages
    messages = systedb.select('conversation', ['*'])
    systedb.close()
    # return messages jsonified

    # convert the messages to a list of dictionaries
    for each in messages:
        conversation.append({
            'role': each[1],
            'content': each[2]
        })

    # return the last 10 messages in the conversation
    return jsonify(conversation[-10:])

# define route to insert messages into the conversation table.
@app.route('/conversation_insert', methods=['POST'])
def conversation_insert():
    systedb = DatabaseManager('bus.db')
    # get data from the request (role, content)
    data = request.get_json()
    role = data['role']
    content = data['content']

    try:
        # insert the data into the conversation table
        systedb.insert('conversation', ['role', 'content'], [role, content])
        systedb.close()
        return "success"
    except Exception as e:
        return str(e)
        

# define route to get the messages from the north bound bus.
@app.route('/north_bound_bus_get', methods=['GET'])
def north_bound_bus_get():
    systedb = DatabaseManager('bus.db')

    # get messages
    messages = systedb.select('north_bound_bus', ['*'])
    systedb.close()
    # return messages jsonified
    return jsonify(messages)


# define route to insert messages into the north bound bus.
@app.route('/north_bound_bus_insert', methods=['POST'])
def north_bound_bus_insert():
    systedb = DatabaseManager('bus.db')
    # get data from the request (layer, messages)
    data = request.get_json()

    layer = data['layer']
    messages = data['messages']

    try:
        # insert the data into the north bound bus
        systedb.insert('north_bound_bus', ['layer', 'messages'], [layer, messages])
        systedb.close()
        return "success"
    except Exception as e:
        return str(e)
    

# define route to get the messages from the south bound bus.
@app.route('/south_bound_bus_get', methods=['GET'])
def south_bound_bus_get():
    systedb = DatabaseManager('bus.db')

    # get messages
    messages = systedb.select('south_bound_bus', ['*'])
    systedb.close()
    # return messages jsonified
    return jsonify(messages)


# define route to insert messages into the south bound bus.
@app.route('/south_bound_bus_insert', methods=['POST'])
def south_bound_bus_insert():
    systedb = DatabaseManager('bus.db')
    # get data from the request (layer, messages)
    data = request.get_json()
    layer = data['layer']
    messages = data['messages']

    try:
        # insert the data into the south bound bus
        systedb.insert('south_bound_bus', ['layer', 'messages'], [layer, messages])
        systedb.close()

        # call the next layer in a thread and return success to the api call
        threading.Thread(target=nxtLayer, args=('aspirational',)).start()
        return {
            "status": "success",
            "message": "posted to the south bound bus",
            "data": messages
        }
        
    except Exception as e:
        print(e)
        return str(e)
    


# Start the Flask application development server
if __name__ == '__main__':
    app.run(debug=True, port=6070, host='0.0.0.0')