from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.llms import GooglePalm
import os
from dotenv import load_dotenv
load_dotenv()

memory = ConversationBufferMemory()
# setting the enviroment key for google api key at the operating system level
os.environ["GOOGLE_API_KEY"] = "AIzaSyB7IXQVFC9PdwRVrntUrJtNxw-RlvUOLFk"

class ContextManager:

    def __init__(self):
        pass
    def _context(self):

        llm=GooglePalm()
        query=input(":>")

        if query=="q":
            os._exit(0)
        else:
            conv = ConversationChain(
                                llm=llm,
                                memory=memory,
                                verbose=True
                                )
        output=conv.predict(input=query)
        memory.save_context({"input": query},
                            {"output": output})

        return output
            # print(history)

context=ContextManager()
while True:
    print(context._context())