
from langchain.agents import initialize_agent, AgentType
from langchain.tools.yahoo_finance_news import YahooFinanceNewsTool
from langchain.agents import initialize_agent
from langchain.llms import GooglePalm

import os
from dotenv import load_dotenv
load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")

# declare Language Model
primary_llm = GooglePalm(
    google_api_key=google_api_key,
    temperature=0.7
    )

tools = [YahooFinanceNewsTool()]
agent_chain = initialize_agent(
    tools,
    llm=primary_llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

def agent_financialAdvisor(query):
    agent_chain.run(query)
