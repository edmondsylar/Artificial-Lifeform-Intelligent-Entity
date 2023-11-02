import threading
import time
import os
import openai
from data import working_memory
from SystemModules.memory_management import _build_memory
from SystemModules.decision import decider
from rich.console import Console
from Tools.image_generation import generate_image
from wrappers.memory import prompt_builder

console = Console()


openai.api_key = os.getenv("OPENAI_API_KEY")


def chat():
    main_instance = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            max_tokens=4000,
            messages=working_memory
        )
    ai_response  = main_instance.choices[0].message
    _build_memory(working_memory, 'assistant', ai_response['content'])
    response = rf"Response: {ai_response['content']}"
    console.print(ai_response['content'])
    return response

@prompt_builder('@USER')
def _interact(user_request):
    return user_request
    

# this will run as a thread.
def _system():
    while True:
        comm = input("\n ALFIE ::>> ")
        comm = _interact(comm)

        # threading.Thread(target=_interact, args=(comm,)).start()
        # build prompt here.
        dc = decider(comm)
        if len(dc['tools']) <= 0:
            _build_memory(working_memory, 'user', comm)
            chat()
        tools = dc['tools']

        for tool in tools:
            if tool == 'image_generation':
                # start the image generation process.
                threading.Thread(target=generate_image, args=(comm)).start()

        str_tools = ", ".join([str(x) for x in tools])
        
        print(tools)
        edited_prompt = f"""
        User Request:
        {comm},

        The system is using these tools in the background to complete the tasks and it share be letting you know.
        Tools:
        {str_tools}.
        
        Please answer accordigly. 

        """
        # print(edited_prompt)
        _build_memory(working_memory, 'user', comm)
        chat()



        # exit(0)


threading.Thread(target=_system).start()