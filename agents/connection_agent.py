# this agent is going to Keep checking is there is an internet connection.
import threading
import requests
from time import sleep
import subprocess


url = "https://google.com"

# we are just going to try and connect to the internet and if we get a successful ping, we are connect.
def _check_connectivity_status():
    # this is going check if we have inernet.
    state = "disconnected"

    try:
        response = requests.get(url=url)
        if response != None:
            state = "connected"
            return state
    except Exception as error:
        print({
            "status":"disconnected",
            "errorMessage": fr"Experiencing an internet downtime Error: {error}"
        })
        state = "disconnected"


while True:
    status = _check_connectivity_status()
    if status != "connected":
        # wait to restart
        sleep(4)
        try:
            subprocess.run("clear", shell=True)
        except:
            subprocess.run("cls")
        continue
    else:
        # connected to the internet
        sleep(300)
        continue
        
        