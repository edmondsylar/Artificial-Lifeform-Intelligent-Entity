import pyttsx3
import argparse
import json
import time
from functions.speech_control import update_switch
from functions.speech_control import check_system_perset
from functions.auto import stream_and_play

# Initialize the parser
parser = argparse.ArgumentParser(description="Text to Speech")
parser.add_argument("text", type=str, help="Text to convert to speech")

# Parse the arguments
args = parser.parse_args()

engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Change voice to female 
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def _speak(text):
    # Update the switch value to True
    update_switch(True)
    engine.say(text)
    engine.runAndWait()

    # Update the switch value to False
    update_switch(False)

# check the system preset to decide which voice to use
preset = check_system_perset()

if preset == "debug":
    _speak(args.text)
elif preset == "production":

    # try to stream and play the audio 
    try:
        stream_and_play(args.text)
    except Exception as e:
        print(e)
        _speak(args.text)