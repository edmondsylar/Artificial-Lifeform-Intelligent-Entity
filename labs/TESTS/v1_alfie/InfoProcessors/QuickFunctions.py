# tool selector
from SystemTools.system_execution import _execution
from SystemTools.agent_sysExec import agent_sysExec
from SystemTools.agent_deepSearch import agent_deepSearch

import json


def json_convert(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        json_result = json.loads(result)
        return json_result
    return wrapper


def _perform(func, *args, **kwargs):
    # Call the function with the given arguments and get the result
    result = func(*args, **kwargs)

def _toolSelector(tool, instruction):
    if tool == "system_execution":
        _perform(_execution, instruction)
    elif tool == "web_crawler":
        agent_sysExec(instruction)

