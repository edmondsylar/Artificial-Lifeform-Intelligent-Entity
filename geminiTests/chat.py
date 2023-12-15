import google.generativeai as genai

genai.configure(api_key="AIzaSyDP20o8c9aoNlns4w49TywukOhXRUNHnxE")

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  }
]

model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

convo = model.start_chat(history=[
  {
    "role": "user",
    "parts": "hi there!"
  },
  {
    "role": "model",
    "parts": "Hello! How can I help you today?"
  },
  {
    "role": "user",
    "parts": "what's your name?"
  }
])

convo.send_message({
    "role": "user",
    "parts": "My Name is Edmond Musiitwa and am a software developer"
  })
# print(convo.last.text)