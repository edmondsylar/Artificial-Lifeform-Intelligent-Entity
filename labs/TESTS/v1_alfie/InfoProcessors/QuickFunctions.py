# tool selector
from SystemTools.system_execution import _execution
from SystemTools.agent_sysExec import agent_sysExec
from SystemTools.agent_deepSearch import agent_deepSearch
from SystemTools.agent_financialAdvisor import agent_financialAdvisor
from SystemTools.agent_CodeSimulator import agent_CodeSimulator

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
        _perform(agent_sysExec, instruction)
    elif tool == "web_crawler":
        _perform(agent_deepSearch, instruction)
    elif tool == "financial_advisor":
        _perform(agent_financialAdvisor, instruction)
    elif tool == "code_generator":
        _perform(agent_CodeSimulator, instruction)
