import threading
import time
import os
import openai
from wrappers.memory import prompt_builder

openai.api_key = os.getenv("OPENAI_API_KEY")

msgs = [
        {"role": "system", "content": "You are a coding agent for an ai system, you receive requests and you using python you build as the system instructs"}
    ]

@prompt_builder('@SYSTEM')
def code_generation(prompt):
    user_msg = {
        'role': 'user',
        'content':f'{prompt}'
    }

    msgs.append(user_msg)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=msgs,
    )

    resp = response.choices[0]['message']['content']
    
    ai_msg = {
        'role': 'assistant',
        'content':f'{resp}'
    }

    msgs.append(ai_msg)

    # return
    return {
            'task': f'Code generation request with prompt:  \n{prompt}',
            'Status': 'Complete',
            'content': resp,
        }
