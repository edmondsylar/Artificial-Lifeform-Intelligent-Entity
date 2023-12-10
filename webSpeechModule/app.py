from flask import Flask, request, send_file, render_template
from werkzeug.utils import secure_filename
import uuid
import os
from controllers.audio_transription import transcribe_audio
import threading
from controllers.ai_assistant import chat
import time

app = Flask(__name__)
transcriptions = [] # a list of all the made transcriptions.

conversation = [] # a list of all the conversations between the user and the online Bot.


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


@app.route('/audio', methods=['POST'])
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

    app.run(debug=True, port=5000)