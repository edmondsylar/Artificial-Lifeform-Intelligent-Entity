from langchain_experimental.agents.agent_toolkits import create_python_agent
from langchain_experimental.tools import PythonREPLTool
from langchain_experimental.utilities import PythonREPL
from langchain.llms import GooglePalm
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType

import os
from dotenv import load_dotenv
load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")

agent_executor = create_python_agent(
    llm=ChatOpenAI(temperature=0, max_tokens=2000),
    tool=PythonREPLTool(),
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)

def agent_CodeSimulator(instruction):
    agent_executor.run(instruction)

# agent_CodeSimulator("build a simple script to tell is the time in python.")