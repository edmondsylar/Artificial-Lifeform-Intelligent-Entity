import speech_recognition

# Create a recognizer object.
recognizer = speech_recognition.Recognizer()

# Set the recognizer's API key.
recognizer.SetCredentials("path/to/service_account.json")

# Set the recognizer's language model.
recognizer.SetLanguageModel("en-US")

# Start the recognizer.
recognizer.StartListening()

# Wait for the recognizer to finish.
while recognizer.IsListening():
    # Get the transcription results.
    transcription = recognizer.GetTranscript()

# Print the transcription results.
print(transcription)

# Stop the recognizer.
recognizer.StopListening()