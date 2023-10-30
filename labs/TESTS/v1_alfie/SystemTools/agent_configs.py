from langchain.agents import initialize_agent, load_tools
from langchain.llms import GooglePalm
from langchain.tools import ShellTool
from langchain.agents import AgentType


import os
from dotenv import load_dotenv
load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")

# declare Language Model
primary_llm = GooglePalm(
    google_api_key=google_api_key,
    temperature=0.2
    )
