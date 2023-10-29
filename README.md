# Project README   

This project is a conversational AI tool that uses Google's generative language model, Palm, to interact with users and perform tasks. It's designed to handle Linux tasks, perform web searches, and generate text based on user prompts.
Setup

1. Clone the repository to your local machine.
2. Install the required Python packages by running pip install -r requirements.txt.
Usage

The main entry point of the application is execution.py. This script prompts the user for input and uses the AI model to generate a response.

To start the application, run python execution.py in your terminal. You will be prompted to enter a command. The AI will then generate a response based on your input.

Here's an example of how to use the application:

The AI will then generate a response, which could be a Linux command, a web search result, or a text generation based on the user's input.
Important Files

- co_pilot.py: This file contains the main AI model and its configuration.
- execution.py: This is the main entry point of the application.
- functions/: This directory contains helper functions for the application.
- labs/TESTS/v1_alfie/: This directory contains test scripts for the application.
Note

Please ensure you have the necessary API keys and environment variables set up for the application to function correctly. The Google API key is required for the Palm model to work. You can set it in the google_api_key variable in the app.py file.
Contributing

Contributions are welcome. Please submit a pull request or open an issue if you have any improvements or suggestions.