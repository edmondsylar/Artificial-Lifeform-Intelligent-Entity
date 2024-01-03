# this is going to the be the gemini file holding google gemini api access
import google.generativeai as gemini

# configure gemini
gemini.configure( api_key='AIzaSyDP20o8c9aoNlns4w49TywukOhXRUNHnxE')

model = gemini.GenerativeModel('gemini-pro')

messages = []

def build_conversation(role, message):
    # build a conversation
    obj = {
        "role": role,
        'parts': [message]
        
    }

    # append to messages
    messages.append(obj)
    

# old implementation of handling conversation in Palm2


while True:
    message = input('user: ')

    # build conversation
    build_conversation('user', message)

    response = model.generate_content(messages)

    # build conversation
    build_conversation('model', response.text)

    print('Model: ', response.text)