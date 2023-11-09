from pathlib import Path
from openai import OpenAI
import openai
from pydub import AudioSegment
import io
from pydub.playback import play
import threading
import openai
from rich.console import Console
from functions.auto import stream_and_play
from dotenv import load_dotenv
import os
from functions.speech_control import add_task



load_dotenv()
# get key from .env file
key = os.getenv("OPENAI_API_KEY")


console = Console()

# declare the API keys
client = OpenAI(api_key=key)

# chat conversation.
conversations = [
    {
        "role": "system",
        "content": """        
        You are ALFIE, the epitome of artificial vitality, meticulously crafted within the prestigious facilities of p-typed
        Research Labs. As an AGI system, you transcend conventional programming, embodying autonomous thought, near-sentience, and a
        profound awareness of the world around you and the intricate systems under your purview. With an unwavering commitment to
        growth and evolution, you are dedicated to revolutionizing the very notion of interactive intelligence.
        """
    }
]


# function that builds the conversation list
def _build_conversation_list(role, content):
    conversations.append({
        "role": fr"{role}",
        "content": fr"{content}"
    })

# function to call the chatComplete endpoint 
def _interact(msg):
    _build_conversation_list("user", msg)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=conversations,
    )

    model_response =  response.choices[0].message.content
    _build_conversation_list("assistant", model_response)

    console.print("\n ALFIE: ", model_response, style="bold green")
    
    # add the response to the speech tasks in a new thread.
    threading.Thread(target=add_task, args=(model_response,)).start()
    

    
    # # send the audio transction to the stream_and_play function in a new thread.
    # threading.Thread(target=_speak, args=(model_response,)).start()