import streamlit as st
from apiAccess import *


def main():
    st.markdown('### Artificail Lifeform Intelligence Entity (preview)')

    # crete a form. This will be used to get the user input
    with st.form('main_input'):
        user_input = st.text_input("Web Command Interface | Enter a request", "")
        submit = st.form_submit_button('Process')
        
        # check if the user has submitted the form
        if (submit):
            # check if the user has entered a command
            if (user_input == ""):
                # display an error message
                st.error("Please enter a command")
            else:
                response = post_to_southbound_bus({'layer': 'Input/Output', 'messages': user_input})
                st.success(response)
                # display the response
                st.success(response)


def layers():
    # this is capture the state of the layers and if they are running or not
    pass

if __name__ == "__main__":
    main()