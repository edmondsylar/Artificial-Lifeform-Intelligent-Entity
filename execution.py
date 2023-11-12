import os
from functions.make_json import jsonify_data
from functions.memory_manager import build_memory, _tempMemory
from co_pilot import _copilot
import time
from functions.systemExec import _system_ai_execution_agent
from rich.console import Console
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.llms import GooglePalm
from dotenv import load_dotenv
load_dotenv()

memory = ConversationBufferMemory()
# setting the enviroment key for google api key at the operating system level                                                                   
# os.environ["GOOGLE_API_KEY"] = "GOOGLE_API_KEY"

console = Console()
def _context(user_prompt, data):
        # managing context

        llm=GooglePalm()
        # creating the conversation chain to hold the current messages

        conversation = ConversationChain(
                                llm=llm,
                                memory=memory,
                                verbose=True
                                )
        # predicting the user response basing on the previus requests

        output=conversation.predict(input=user_prompt)
        memory.save_context({"input": user_prompt},
                            {"output": data})

        return output

while _tempMemory != None:
    user_prompt = input(":> ")
    if user_prompt == "exit":
        break
    else:
        response = _copilot(user_prompt)
        # print(response.result)
        data = str(response.result)
        console.print(_context(user_prompt, data))
        # console.print(data)
        


