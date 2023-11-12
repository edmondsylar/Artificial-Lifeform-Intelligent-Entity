from langchain.agents import initialize_agent, load_tools
from langchain.agents import load_tools, initialize_agent, AgentType
from langchain.llms import GooglePalm

import os
from dotenv import load_dotenv
load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")


llm = GooglePalm(
    google_api_key=google_api_key,
    temperature=0.7
    )

tools = load_tools(
    ["arxiv"],
)

agent_chain = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

agent_chain.run(
    "give me a summery of this paper please '2310.08560' "
)