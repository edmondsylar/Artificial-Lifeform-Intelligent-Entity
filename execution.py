import os
from functions.make_json import jsonify_data
from functions.memory_manager import build_memory, _tempMemory
from co_pilot import _copilot
import time
from functions.systemExec import _system_ai_execution_agent
from rich.console import Console

console = Console()

while _tempMemory != None:
    user_prompt = input(":> ")
    if user_prompt == "exit":
        break
    else:
        response = _copilot(user_prompt)
        # print(response.result)
        data = jsonify_data(response.result)
        console.print(data)
        


