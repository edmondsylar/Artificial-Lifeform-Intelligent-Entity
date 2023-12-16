# this is going to have temporary memory using a simple list.
import google.generativeai as genai
from gtts import gTTS
import random
import pathlib
from pydub import AudioSegment
from pydub.playback import play
from speech_engine import whisperSpeech
from rich.console import Console
import threading
import os
import time
import pyaudio
from io import BytesIO
import threading
import sys
import datetime
import json

# initialize the console
console = Console()

# initialize the genai api
genai.configure(api_key="AIzaSyCtGFwP8vcxz_qWlqU932IP_s7AsAghpvw")

# initialize the temp memory
_temp_memory = []

# Set up the model
model = genai.GenerativeModel(model_name="gemini-pro")

# Start a conversation
convo = model.start_chat()

# define the function to build the memory
def build_memory(response, role ):
   data = {
      "response": response,
      "role": role,
      "time": f"{datetime.datetime.now()}",
   }
   _temp_memory.append(data) # append to the list



def write_memory_to_file():
    # Load existing data
    with open('memory.json', 'r') as f:
        data = json.load(f)

    # Append new data
    data.extend(_temp_memory)

    # Write data back to file
    with open('memory.json', 'w') as f:
        json.dump(data, f)


def get_multiline_input():
  """Gets multiline input from the user.

  The user can enter multiple lines of input, and the function will only return
  when the user presses Ctrl+Return.
  """

  lines = []
  while True:
    line = sys.stdin.readline()
    if line == "\n":
      break
    lines.append(line)
  return "".join(lines)



def memory_saver_loop():
    while True:
        write_memory_to_file()
        # print("Memory Saved")

        time.sleep(20)
        # clear screen with os.system('cls') on windows
        # os.system('cls')


def load_memory():
    with open('memory.json', 'r') as f:
        virtualMem = json.load(f)

        HistoryContext = 'Conversation Hsistory is still loading... and will be availabe soon.'
        last_5_msgs = virtualMem[-5:]

        continuation = fr'''

        # History Context
        {HistoryContext}

        # Last 5 Messages
        {last_5_msgs}

        # Note
        The history and the last 5 messages can be empty if there is no prior conversation history. 

        '''
    return continuation

def play_response_audio(response):
    threading.Thread(target=whisperSpeech, args=(response,)).start()


def startUp():
    console.log('Starting up...')
   #load the memory
    memory = load_memory()

    startUpMesg = fr'''
    This is a system boot up.
    Time: {datetime.datetime.now()}
    Working Directory: {pathlib.Path().absolute()}

    # Memory
    {memory}

    # Instructions.
    This is your previous conversation history, had with the user.
    User it to the best of your ability to undersatnd the user and respond to them accordingly.


    #Note this is a system message or call it your inner thought and you can respond by starting the conversation with a Greating to the user in context of the all the information you have.
    '''

    try:
        # make the call to the api
        console.log(startUpMesg[-15000:])
        
        convo.send_message(startUpMesg[-15000:])
        console.log(convo.last.text)

        build_memory(convo.last.text, "system")
        play_response_audio(convo.last.text)
    except Exception as e:

        console.log(startUpMesg[-15000:])

        # convert error to string
        e = str(e)
        # get the last 300 characters of the error
        e = e[-15000:]

        msg = fr'''
            Experieneing an error while starting up.
            Error: {e}
        '''
        console.log(msg)
        convo.send_message(msg)
        build_memory(convo.last.text, "system")
        play_response_audio(convo.last.text)
        
        console.log(e)


    


# start the startup function
startUp()

time.sleep(2)
# start the memory saver loop
threading.Thread(target=memory_saver_loop).start()

# while True...
while True:
    # Get a message from the user
    msg = input("You: ")
    # Send a message

    # build the memory
    build_memory(msg, "user")

    if msg != "":
        msg = fr'''
        You only Response to the Query passed
        
        User Query : {msg}

        # instructions.
        You are Alfie (ALFIE - Artificial Lifeform Intelligent Entity) an AGI System that is being built to understand and interact with humans. all the responses.
        you are giving are going to be in the form of speech not necessarily text so you will need to ensure your responses are in the form of speech because the system is going to convert them to speech.

        Note: please don't introduce yourself unless you are asked to do so, the 'instructions' are just for you to ground your responses and interactions.

        '''
        convo.send_message(msg)
        # Get the response
        console.log(convo.last.text)

        # build the memory
        build_memory(convo.last.text, "system")

        # play the response
        play_response_audio(convo.last.text)
