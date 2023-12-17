# Activate the conda environment
conda activate alfie_base

# Run each of the layers in ACE/layer/Gemini/geminiSupport.py
nohup python ACE/AspirationalLayer/GeminiSupport/GeminiSupport.py &> /dev/null &
nohup python ACE/GlobalStrategyLayer/GeminiSupport/GeminiSupport.py &> /dev/null &
nohup python ACE/AgentModelLayer/GeminiSupport/GeminiSupport.py &> /dev/null &
nohup python ACE/ExecutiveFunctionsLayer/GeminiSupport/GeminiSupport.py &> /dev/null &
nohup python ACE/CognitiveControl/GeminiSupport/GeminiSupport.py &> /dev/null &
nohup python ACE/TaskProsecution/GeminiSupport/GeminiSupport.py &> /dev/null &

# # Start the database server api in the systemApis folder
# nohup python systemApis/app.py &> /dev/null &

# # Start the web interface for the system from the Frontend folder
# nohup streamlit run Frontend/webInterface.py &> /dev/null &

# # Start the webspeech api in the webspeechModule folder
# nohup python webspeechModule/app.py &> /dev/null &