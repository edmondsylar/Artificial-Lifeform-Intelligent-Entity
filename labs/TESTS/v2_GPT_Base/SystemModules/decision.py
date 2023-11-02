# this is a simple openai funciton to help use decide on which tool to call.
import time
import os
import openai
from rich.console import Console
import json

console = Console()

tools = f"""
image_generation: This tool assists in Generating pictures
code_genaration: This tool assists in generating code.
"""

initial_command = f""" You are a decider module in an ai system, your only roles is to check thorough the list of all the tools you have and you can reply to the "system_demand" with a list of tools required to complete the request.
if you have no tool for the requested tasks, please always return and empty tools List, and an instruction to create that required tool

These are the tools:
{tools}

Your response format is strictly as below:

{{
    "tools": [list of tools required to complete the request],
    "instruction": ""
}}.


"""

# key : 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
openai.api_key = os.getenv("OPENAI_API_KEY")

def decider(query):

    qu = f"""
    {initial_command}

    system_demand: {query}
    """

    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=qu,
        max_tokens=250
    )

    tool_response = json.loads(response['choices'][0]['text'])
    # console.print(tool_response, type(tool_response))
    return tool_response
    

def prompt_builder(user_prompt):
    pass