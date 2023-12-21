from flask import Flask, request, send_file, render_template
from werkzeug.utils import secure_filename
import uuid
import os
from controllers.audio_transription import transcribe_audio
import threading
from controllers.ai_assistant import chat
import time
import requests

app = Flask(__name__)
transcriptions = [] # a list of all the made transcriptions.

conversation = [] # a list of all the conversations between the user and the online Bot.

# orchestrator url
orchestrator_url = "http://localhost:5007/sound_input"
orchestrator_url_keyboard = "http://localhost:5007/keyboard_input"

# function sends the transcription to the orchestrator
def sharetranscription(transcription):
    data = {
        "speech_to_text": transcription
    }

    try:
        response = requests.post(orchestrator_url, json=data)
        return response.json()
    except Exception as e:
        print(e)
        return {
            "message": "Error Occured!", 
            "status": 400, 
            "error": e
            }


def shareKeyBoardInput(keyboard_input):
    data = {
        "keyboard_input": keyboard_input
    }

    try:
        response = requests.post(orchestrator_url_keyboard, json=data)
        return response.json()
    except Exception as e:
        print(e)
        return {
            "message": "Error Occured!", 
            "status": 400, 
            "error": e
            }

def build_conversation(msg):
    conversation.append(msg)

    if len(conversation) > 15:
        return conversation[14:]
    else:
        return conversation

    

# file delete function
def delete_file(filename):
    # sleep for 10 seconds before deleting the file
    time.sleep(10)

    os.remove(filename)
    print(f"File {filename} removed successfully!")
    return True


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        audio_file = request.files["audio_data"]
        filename = secure_filename(audio_file.filename)
        audio_file.save(f"recordings/{filename}")
        return {"message": "Audio recording saved successfully!"}
    

# dashboard route calling the dashboard.html file
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# define text input endpoint.
@app.route('/text_input', methods=['POST'])
def text_input():
    data = request.get_json()
    
    # pass the text to the orchestrator as a thread
    # call the orchestrator here and pass the text to it.
    threading.Thread(target=shareKeyBoardInput, args=[data['system_prompt']]).start()

    return "complete"
   

@app.route('/audio', methods=['POST'])
def handle_audio():
    audio_file = request.files['audio']
    filename = secure_filename(audio_file.filename)
    temp_filename = str(uuid.uuid4()) + filename
    audio_file.save(temp_filename)
    ai_response= None

    try:
        # Here you can process the audio file
        # For example, you can pass it to a transcription function
        transcription = transcribe_audio(temp_filename, transcriptions)

        # check the transcription returned from the function
        if transcription:
            transcriptions.append(transcription.text)

            # share the transcription with the orchestrator as a thread
            threading.Thread(target=sharetranscription, args=[transcription.text]).start()
            
            # build the conversation
            conversation = build_conversation(transcription.text)

            # pass the conversation to the chat function
            ai_response = chat(conversation)

            build_conversation(fr'{ai_response}')

            # print(transcription.text, "AI:\n ", ai_response)  # Access 'text' attribute using dot notation
        else:
            # print(transcription)
            return 'Audio not processed', 400

        return {
            "message": "Audio recording saved successfully!",
            "transcription": transcription.text,
            "ai_response": ai_response
        }, 200
        
    finally:
        # Delete the temporary file
        # delete_file(temp_filename)
        return {
            "message": "Audio recording saved successfully!",
            "transcription": transcription.text,
            "ai_response": ai_response
        }, 200


if __name__ == "__main__":

    # monitor for the (Ctrl + C) command to stop the server
    try:
        print("Server is running...")
    except KeyboardInterrupt:
        print("Server is shutting down...")
        time(10)
        
        
        
        exit(0)

    app.run(debug=True, port=5008)