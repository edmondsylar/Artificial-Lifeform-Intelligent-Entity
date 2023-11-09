import pyttsx3
import threading

engine = pyttsx3.init()
engine.setProperty('rate', 150)

# change voice to female 
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def _speak(text):
    engine.say(text)
    engine.runAndWait()
    
