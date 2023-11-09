import subprocess
import threading

def run_vocals(text):

    string = fr".. {text} .."

    print(string)

    command = fr'python vocals.py "{text}"'
    subprocess.run(command, shell=True)
