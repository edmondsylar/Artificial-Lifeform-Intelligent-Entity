from langchain.chat_models import ChatGooglePalm
from langchain import hub

# primary imports
from langchain.tools.render import render_text_description
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain.agents.format_scratchpad import format_log_to_str
from langchain import hub


from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent
import os
from langchain.agents import AgentExecutor


from langchain.agents.output_parsers import JSONAgentOutputParser
from langchain.agents.format_scratchpad import format_log_to_messages
from dotenv import load_dotenv

load_dotenv()

serpapi_api_key = os.getenv("SERPAPI_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")

# set the serp api key
os.environ["SERPAPI_API_KEY"] = serpapi_api_key

search = SerpAPIWrapper()
tools = [
    Tool(
        name="Current Search",
        func=search.run,
        description="useful for when you need to answer questions about current events or the current state of the world"
    ),
]


prompt = hub.pull("hwchase17/react-chat-json")
llm = ChatGooglePalm(
                    temperature=0.5, 
                    google_api_key=google_api_key
                    )

prompt = prompt.partial(
    tools=render_text_description(tools),
    tool_names=", ".join([t.name for t in tools]),
)

chat_model_with_stop = llm.bind(stop=["\nObservation"])

# We need some extra steering, or the chat model forgets how to respond sometimes
TEMPLATE_TOOL_RESPONSE = """TOOL RESPONSE: 
---------------------
{observation}

USER'S INPUT
--------------------

Okay, so what is the response to my last comment? If using information obtained from the tools you must mention it explicitly without mentioning the tool names - I have forgotten all TOOL RESPONSES! Remember to respond with a markdown code snippet of a json blob with a single action, and NOTHING else - even if you just want to respond to the user. Do NOT respond with anything except a JSON snippet no matter what!"""

agent = {
    "input": lambda x: x["input"],
    "agent_scratchpad": lambda x: format_log_to_messages(x['intermediate_steps'], template_tool_response=TEMPLATE_TOOL_RESPONSE),
    "chat_history": lambda x: x["chat_history"],
} | prompt | chat_model_with_stop | JSONAgentOutputParser()

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True, memory=memory) 

agent_executor.invoke({"input": "Hi there, how are you?"})['output']
