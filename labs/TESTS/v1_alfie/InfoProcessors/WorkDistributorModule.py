import json
# this file is going to have the work_distribution_engine.
from SystemTools.system_execution import _execution
from InfoProcessors.QuickFunctions import _toolSelector

active_tools = []

def grow_tools(tools):
    for tool in tools:
        # check is the passed tool exists in the list if not, add it.
        if tool not in active_tools:
            active_tools.append(tool)
            

def _receiver(tools, instruction):
    # grow toold first.
    grow_tools(tools)

    # check for tools and perform actions here.
    for _t in tools:
        if _t in active_tools:
            # pass the tool and the instruction to the _toolSelector.
            _toolSelector(_t, instruction)

            

    print(f"take action with the following tools {tools} and follow these instructions {instruction}")
    return True





