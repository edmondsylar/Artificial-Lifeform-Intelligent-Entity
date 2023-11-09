import speech_recognition as sr
import threading
# import keyboard

def Linsten():
    # obtain the audion from the microphone
    speech = ""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
        # recognize speech using Sphinx
    try:
        speech = r.recognize_google(audio)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    return speech


while True:
    # "Triggered the listenner"
    # threading.Thread(target=Linsten).start()
    instructions = Linsten()

    # convert to a lower case string
    instructions = instructions.lower()

    # check if the string got the word "alfie" or "hey buddy"
    if 'alfie' in instructions or 'hey buddy' in instructions:
        print(instructions)

    else:
        print("ignoring convesation: {}".format(instructions))

