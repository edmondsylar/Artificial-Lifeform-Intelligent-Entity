from langchain.agents import initialize_agent, load_tools
from langchain.llms import GooglePalm
from langchain.tools import ShellTool
from langchain.agents import AgentType

from langchain.tools import DuckDuckGoSearchResults
from langchain.tools import DuckDuckGoSearchRun

import os
from dotenv import load_dotenv
load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")

# 
search = DuckDuckGoSearchRun()

shell_tool = ShellTool()

shell_tool.description = shell_tool.description + f"args {shell_tool.args}".replace(
    "{", "{{"
).replace("}", "}}")

# declare Language Model
primary_llm = GooglePalm(
    google_api_key=google_api_key,
    temperature=0.2
    )

def agent_sysExec(query):
    agent = initialize_agent(
        [shell_tool],
        agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        llm=primary_llm,
        verbose=True,
        handle_parsing_errors=True
    )
    agent.run(query)


