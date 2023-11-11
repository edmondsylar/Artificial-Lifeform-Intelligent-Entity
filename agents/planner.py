import os
from langchain.llms import VertexAI
from langchain.chat_models import ChatVertexAI
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.tools import ShellTool
from langchain.agents import AgentExecutor
from dotenv import load_dotenv
from langchain.llms.google_palm import GooglePalm
from langchain.llms import OpenAI
from langchain.utilities import SerpAPIWrapper
from langchain.agents import Tool
from langchain.agents.output_parsers import SelfAskOutputParser
from langchain.agents.format_scratchpad import format_log_to_str
from langchain import hub


# initialize the shell tool
shell_tool = ShellTool()

load_dotenv()

# get key from .env file
key = os.getenv("GOOGLE_NLP_KEY")
# Initialize the language model

# set the key in the environment
os.environ['GOOGLE_API_KEY'] = key

# set serpapi key in the environment
os.environ['SERPAPI_API_KEY'] = os.getenv("SERPAPI_KEY")


llm = GooglePalm()


# llm = OpenAI(temperature=0)
search = SerpAPIWrapper()
shell = ShellTool()

tools = [
    Tool(
        name="Intermediate Answer",
        func=search.run,
        description="useful for when you need to ask with search",
    ),
    Tool(
        name="Shell",
        func=shell_tool.run,
        description="useful for when you need to run a shell command",
    ),
]

prompt = hub.pull("hwchase17/self-ask-with-search")

llm_with_stop = llm.bind(stop=["\nIntermediate answer:"])



agent = (
    {
        "input": lambda x: x["input"],
        # Use some custom observation_prefix/llm_prefix for formatting
        "agent_scratchpad": lambda x: format_log_to_str(
            x["intermediate_steps"],
            observation_prefix="\nIntermediate answer: ",
            llm_prefix="",
        ),
    }
    | prompt
    | llm_with_stop
    | SelfAskOutputParser()
)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
agent_executor.invoke(
    {"input": "who won the balon d'or in 2023?, also kindly check if my windows has any servives running."}
)