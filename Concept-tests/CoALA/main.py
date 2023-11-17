# python class called COALA. we are going to use google-generativeai (PalM2) as the api for this one
# we are using the json files [thoughts.json, memory.json] to store the data and we need a function to read and write to them (memoryManager)

import os
import threading
import time
import random
import json
from dotenv import load_dotenv

# import rich for the console
from rich.console import Console

# import google-generativeai (PalM2) api
import google.generativeai as palm

# define the console
console = Console()

# load the .env file
load_dotenv()

# get the api key from the .env file
key = os.getenv("GOOGLE_API_KEY")

palm.configure(api_key=key)

# replace the print function with the console.log function
def print(*args, **kwargs):
    console.log(*args, **kwargs)


# 

# COALA class
class COALA:
    def __init__(self, bot_name):
        self.name = bot_name
        self.memory = []
        self.thoughts = []
        self.prompt = ""
        self.time_started = time.time()

        # aiBotMainInstance defaults.
        self.defaults1 = {
            'model': 'models/chat-bison-001',
            'temperature': 0.9,
            'candidate_count': 1,
            'top_k': 40,
            'top_p': 0.95,
        }

        self.aiBotcontext = """
        You are an autonomous self-thinking evolving ai system. built on top of a language model, you utilize this information to understand the world, you are free thinking and your thoughts are always growing, you periodically will receive \"messages\" from your inner self just to ponder and understand the world better.
        """
    

        # initialize the memory and thoughts
        self.initialize()


    def _aiBotMainInstance(self):

        # make the request to the api
        response = palm.chat(
            **self.defaults1,
            context=self.aiBotcontext,
            examples=[],
            messages=self.memory,
        )

        # print the response
        print(response)
        



    def _promptBuilder(self, UserPrompt):
        pass


    
    # initialize the memory and thoughts
    def initialize(self):
        # this function reades the json files and stores them in the memory and thoughts variables
        self._thoughts_MemoryManager()
        self._memory_MemoryManager()



    def _thoughts_MemoryManager(self):
        if len(self.thoughts) == 0:
            # read the json file and store the "thoughts" item in the thoughts variable
            with open("thoughts.json", "r") as thoughts_file:
                thoughts_data = json.load(thoughts_file)
                self.thoughts = thoughts_data["thoughts"]
            print("Completed reading and writing to thoughts.")
        pass



    def _memory_MemoryManager(self, message=None, option="read"):
        if len(self.memory) == 0:
            # read the json file and store it in the memory variable
            with open("memory.json", "r") as memory_file:
                memory_data = json.load(memory_file)
                self.memory = memory_data["working_memory"]
                print("Completed reading and wrting to memory.")

        # if option == "write":



    def _interface(self):
        # this function is the interface between the user and the bot
        # it takes the input from the user and returns the output from the bot
        
        user_input = input("You: ")
        # append the user input to the memory
        self.memory.append(user_input)

        # call the aiBotMainInstance function
        self._aiBotMainInstance()

        return user_input


# COALA class end
alfie = COALA("alfie")
while True:
    alfie._interface()
    
