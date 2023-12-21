import google.generativeai as genai
import os
import time
import requests
import threading
from dotenv import load_dotenv
from rich.console import Console

# console
console = Console()

# load .env file
load_dotenv()

# gemini api key
gemini_key = os.getenv('google_gemini_api_key')


genai.configure(api_key=' ')


class OrcSupport:
    def __init__(self):
        self.model = None
        self.current_content = None

        self.model = genai.GenerativeModel('gemini-pro')
        self.chat = self.model.start_chat()

    def _interact(self, thoughts, message):

        prompt = fr"""
        # system prompt
        {message}

        # Currently Processed thoughts
        {thoughts}

        #instruuction
        The above is amessage from the orchestrator unit os an agi system, your role is to provide understanding and build context as the interation progresses.
        you strictly respond with the format below:

        {{
            "Deep understanding of the message": "This is a deep understanding of the message",
            "Context": "This is the context of the message"
        }}
        """

        
        response = self.chat.send_message(prompt)
        return response.text
    