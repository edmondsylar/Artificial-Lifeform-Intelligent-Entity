import json
import time
from functions.systemExecutor import run_vocals
import subprocess


def update_switch(state):
    with open('switch.json', 'r+') as f:
        data = json.load(f)
        data['switch'] = state
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()


def add_task(task):

    # convert task to a string
    task = str(fr"{task}")

    with open('switch.json', 'r+') as f:
        data = json.load(f)
        data['tasks'].append(task)
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()


def remove_task(task):
    with open('switch.json', 'r+') as f:
        data = json.load(f)
        data['tasks'].remove(task)
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()


def check_switch():
    with open('switch.json', 'r') as f:
        data = json.load(f)
        return data.get('switch', False)
    

def _run_speech_Control_engine():
    while True:
        print("Alfie: Speech Control Engine Running...")
        if not check_switch():
            with open('switch.json', 'r') as f:
                data = json.load(f)
                tasks = data.get('tasks', [])
                if tasks:
                    task = tasks[0]
                    run_vocals(task)
                    remove_task(task)
        time.sleep(2)
        # clear the screen
        # subprocess.run("clear")

def update_system_preset(value):
    with open('switch.json', 'r+') as f:
        data = json.load(f)
        data['system_preset'] = value
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()


def check_system_preset():
    with open('switch.json', 'r') as f:
        data = json.load(f)
        return data.get('system_preset', "")