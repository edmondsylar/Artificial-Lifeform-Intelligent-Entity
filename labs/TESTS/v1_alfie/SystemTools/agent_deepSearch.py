
from langchain.tools import DuckDuckGoSearchResults
from langchain.tools import DuckDuckGoSearchRun
from .agent_configs import *
from langchain.agents import AgentType

search = DuckDuckGoSearchRun()

# create the agent and run 
def agent_deepSearch(query):
    agent = initialize_agent(
        [search],
        agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        llm=primary_llm,
        verbose=True,
        handle_parsing_errors=True
    )
    agent.run(query)
