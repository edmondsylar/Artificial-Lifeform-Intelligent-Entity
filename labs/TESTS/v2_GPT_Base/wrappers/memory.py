from rich.console import Console
import threading
from Tools.SystemCommunicationsV2 import Toaster
import time

console = Console()
lister = []

def memory_wrapper(func):
    def wrapper(*args, **kwargs):

        # the response from the function.
        response = func(*args, **kwargs)
        time.sleep(5)
        Notification = f"Tasks Complete Task:\n{response}"
        threading.Thread(target=Toaster, args=(Notification, )).start()
        
        return response
    return wrapper
