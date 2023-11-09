import threading

from functions.speech_control import _run_speech_Control_engine
from graphical_user_access import _run_graphical_user_input
from speech_engine import start_speech_recognition

# we are going to run the speech engine in a separate thread
threading.Thread(target=_run_speech_Control_engine).start()

# we are going to run the speech recognition engine in a separate thread
threading.Thread(target=start_speech_recognition).start()


# start the graphical user input in the main thread
_run_graphical_user_input()


while True:
    print("Running main app...")
    input("Press enter to continue...")