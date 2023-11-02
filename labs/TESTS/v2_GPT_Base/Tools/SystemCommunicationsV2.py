import time
from winotify import Notification, audio
import threading

import random
import string

def random_string(length):
    # create a list of all possible characters
    chars = list(string.ascii_letters + string.digits + string.punctuation)
    # shuffle the list randomly
    random.shuffle(chars)
    # pick a random number of characters from the list
    result = random.choices(chars, k=length)
    # join the characters into a string and return it
    return "Generated Random String \n ".join(result)


url = "https://images.theconversation.com/files/374303/original/file-20201210-18-elk4m.jpg?ixlib=rb-1.1.0&rect=0%2C22%2C7500%2C5591&q=45&auto=format&w=926&fit=clip"
def Toaster(message):
    toast = Notification(
        app_id="A.L.F.I.E",
        title="System Notification",
        msg=message,
        icon=r"D:\PTYPED\alfie.png",
        duration="short"
    )
    
    # toast.add_actions(label="Open github", launch=f"{url}")
    # toast.set_audio(audio., loop=False)
    toast.show()

# while True:
#     notification = input("\n Toast: ")
#     threading.Thread(target=Toaster, args=(notification, )).start()