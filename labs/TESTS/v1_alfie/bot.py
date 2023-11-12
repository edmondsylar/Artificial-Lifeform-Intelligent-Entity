import openai
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.llms import GooglePalm, google_palm

from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
import os
from MotalFunctions.FrontalLobe import  frontal_lobe
from MotalFunctions.RequestBuilder import refine_request
from rich.console import Console


openai.api_key = os.getenv("OPENAI_API_KEY")
console = Console()

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
# openai_api_key = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(
    temperature=0.55,
    # api_key=google_api_key
)

# Prompt
prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(
            "You are a central Processing AI Unit for a Big Systsem. You process information provided to you by the system and give the user the appropriate responses to their request, for requests that where your supporting tools have not given an immediate answer please let the user know you are going to be providing the information soon as the ai agents will be sharing information with you to ensure all requests are completed efficiently. your name is ALFIE (ARTIFICIAL LIFEFORM INTELLIGENT ENTITY)"
        ),
        # The `variable_name` here is what must align with memory
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{question} \n "),
    ]
)

# Notice that we `return_messages=True` to fit into the MessagesPlaceholder
# Notice that `"chat_history"` aligns with the MessagesPlaceholder name
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
conversation = LLMChain(llm=llm, prompt=prompt, verbose=True, memory=memory)

# Notice that we just pass in the `question` variables - `chat_history` gets populated by memory
while True:
    UserInput = input("User :")
    fr = frontal_lobe(UserInput)
    refined_user_resquest = refine_request(user_request=UserInput, frontalLobe_response=fr)

    # console.print(refined_user_resquest)
    chat = conversation(
        {"question": f"{refined_user_resquest}"})
    console.print(chat['text'])