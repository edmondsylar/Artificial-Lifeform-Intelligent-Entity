from rich.console import Console
import threading
from Tools.SystemCommunicationsV2 import Toaster
import time

console = Console()
lister = []

def build_prompt(role, func):
    if role == '@SYSTEM':
        apendix = "This is a system Message Please let the user know of this update. \n@SYSTEM"
    elif role == '@USER':
        apendix = "This is a message from the user.\n@SYSTEM"
        # create the wrapper now.
    def wrapper(*args, **kwargs):
        
        # get the function output
        output = func(*args, **kwargs)
        response = fr"{output}. \n \n{apendix}"
        console.log(response)          
        return response
    return wrapper

def prompt_builder(role):
    if role == '@SYSTEM':
        apendix = "This is a system Message Please let the user know of this update. \n@SYSTEM"
    elif role == '@USER':
        apendix = "This is a message from the user.\n@SYSTEM"

    # create wrappers here.
    def wrapper(func):
        def wrapper_inner(*args, **kwargs):
            output = func(*args, **kwargs)
            response = fr"{output}. \n \n{apendix}"
            console.log(response)          
            return response
        return wrapper_inner
    return wrapper
