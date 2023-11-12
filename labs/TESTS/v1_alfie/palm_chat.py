from langchain_experimental.agents.agent_toolkits import create_python_agent
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.memory import ConversationBufferWindowMemory

from langchain.llms import GooglePalm
from langchain.agents.agent_types import AgentType
from langchain.chains import ConversationChain
import os
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
from langchain.memory import ConversationSummaryMemory

load_dotenv()

memory = ConversationBufferWindowMemory(k=1)
memory.save_context({"input": "hi"}, {"output": "whats up"})
memory.save_context({"input": "not much you"}, {"output": "not much"})
memory.load_memory_variables({})


google_api_key = os.getenv("GOOGLE_API_KEY")

llm = GooglePalm(
    temperature=0.55,
    api_key=google_api_key
)
memory = ConversationSummaryMemory(llm=llm)
memory.save_context({"input": "hi"}, {"output": "whats up"})
memory.save_context(
    {"input": "im working on better docs for chatbots"},
    {"output": "oh, that sounds like a lot of work"},
)
memory.save_context(
    {"input": "yes, but it's worth the effort"},
    {"output": "agreed, good docs are important!"},
)

print(memory.load_memory_variables({}))