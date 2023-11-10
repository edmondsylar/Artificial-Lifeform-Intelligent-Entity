import google.generativeai as palm
from rich.console import Console
from dotenv import load_dotenv
import os
import argparse
import json
import threading
from TextInput import _use_command_line


# Initialize the parser
parser = argparse.ArgumentParser(description="User request to the system")
parser.add_argument("UserRequest", type=str, help="request or command to analyze")

# Parse the arguments
args = parser.parse_args()

load_dotenv()
# get key from .env file
key = os.getenv("GOOGLE_NLP_KEY")

console = Console()

palm.configure(api_key=key)



defaults = {
  'model': 'models/text-bison-001',
  'temperature': 0.7,
  'candidate_count': 1,
  'top_k': 40,
  'top_p': 0.95,
  'max_output_tokens': 1024,
  'stop_sequences': [],
  'safety_settings': [{"category":"HARM_CATEGORY_DEROGATORY","threshold":1},{"category":"HARM_CATEGORY_TOXICITY","threshold":1},{"category":"HARM_CATEGORY_VIOLENCE","threshold":2},{"category":"HARM_CATEGORY_SEXUAL","threshold":2},{"category":"HARM_CATEGORY_MEDICAL","threshold":2},{"category":"HARM_CATEGORY_DANGEROUS","threshold":2}],
}


def _required_input(user_request):    

    prompt = f"""you system module in an AGI system, you role is to respond with the most appropriate input tool required on the list of input tools availed to you.
    This list of tools can be updated according to the developers as more capabilities are availed to you.

    Tools:
    text_input: This tools let's the user add provide text input.
    image_input: This lets the user provide image input
    video_upload: Let's you upload a video to the system.

    your response style and format it strictly the input methods required.
    Response Format: 

    {{
    "tools":[]
    }}
    or 

    {{
    "tools":["video_input", "image_input"]
    }}
    or 

    {{
    "tools":["text_input"]
    }}
    input: hi there
    output: {{
    "tools":[]
    }}
    input: go back to garner friedman into it listed nice decks game in was in missouri at gotta it and musk then naturally bar
    output: {{
    "tools":[]
    }}
    input: {user_request}
    output:"""
    response = palm.generate_text(
    **defaults,
    prompt=prompt
    )

    return response.result



# /received hte user request from the terminal and pass it to the required_input function
user_request = args.UserRequest
response = _required_input(user_request)

# convert to json
response = json.loads(response)


if isinstance(response, dict):
    # get the tools list from the response
    tools = response.get("tools", [])
    # the tools list not empty
    if tools:
        # loop through the tools list and print the tools
        for tool in tools:
            if tool == "text_input":
                # call the text_input function in a new thread and close the current thread
                threading.Thread(target=_use_command_line).start()
                exit()
                
    else:
        exit()