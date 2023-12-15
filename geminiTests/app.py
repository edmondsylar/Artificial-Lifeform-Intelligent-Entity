import pathlib
import textwrap

import google.generativeai as genai

genai.configure(api_key="AIzaSyCtGFwP8vcxz_qWlqU932IP_s7AsAghpvw")


def to_markdown(text):
    return textwrap.dedent(text).strip()


def get_models():
    for m in genai.list_models():
        print(m.name)

BasicModel = genai.GenerativeModel(model_name="gemini-pro")

while True:
    text = input("You: ")
    if text == "quit":
        break
    response = BasicModel.generate_content(text)
    print(to_markdown(response.text))
    print("\n\\n")


# response = BasicModel.generate_content("I have noticed the new gemini model doesn't support passing context to the model. how can we now pass context to the model in order to get the best results?")
# print (response.text)