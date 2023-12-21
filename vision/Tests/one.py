import cv2
import base64
import os
import requests
import time
from openai import OpenAI
from collections import deque
from datetime import datetime
import google.generativeai as gemini
import os
from dotenv import load_dotenv

# load .env file
load_dotenv()

# gemini api key
gemini_key = os.getenv('google_gemini_api_key')

# configure gemini
gemini.configure(api_key=' ')

# we are going to use the geminin vision model

def encode_image_to_base64(frame):
    _, buffer = cv2.imencode(".jpg", frame)
    return base64.b64encode(buffer).decode('utf-8')

def send_frame_to_gpt(frame, previous_texts, client):
    # Combine texts and timestamps from the last 5 frames to create context
    context = ' '.join(previous_texts)
  
    # Prepare message payload for sending the frame to GPT
    # Evaluate if the previous prediction matches the current situation from the context,
    # and instruct to make the next prediction
    prompt_message = f"Context: {context}. Assess if the previous prediction matches the current situation. Current: explain the current situation in 10 words or less. Next: Predict the next situation in 10 words or less."

    PROMPT_MESSAGES = {
        "role": "user",
        "content": [
            prompt_message,
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{frame}"}}
        ],
    }

    # Parameters for API call
    params = {
        "model": "gpt-4-vision-preview",
        "messages": [PROMPT_MESSAGES],
        "max_tokens": 500,
    }

    # Make the API call
    result = client.chat.completions.create(**params)
    return result.choices[0].message.content

def main():
    # Initialize OpenAI client
    client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

    # Open PC's internal camera
    video = cv2.VideoCapture(0)

    # Queue to hold the texts of the most recent 5 frames
    previous_texts = deque(maxlen=5)

    while video.isOpened():
        success, frame = video.read()
        if not success:
            break

        # Encode the frame in Base64
        base64_image = encode_image_to_base64(frame)

        # Get the current timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Send the frame to GPT and get the generated text
        generated_text = send_frame_to_gpt(base64_image, previous_texts, client)
        print(f"Timestamp: {timestamp}, Generated Text: {generated_text}")

        # Add the text with timestamp to the queue
        previous_texts.append(f"[{timestamp}] {generated_text}")

        # Wait for 1 second
        time.sleep(1)

    # Release the video
    video.release()

if __name__ == "__main__":
    main()