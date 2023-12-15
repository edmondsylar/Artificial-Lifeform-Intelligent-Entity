nohup python ACE/AspirationalLayer/app.py &> /dev/null &
nohup python ACE/GlobalStrategyLayer/app.py &> /dev/null &
nohup python ACE/AgentModelLayer/app.py &> /dev/null &
# nohup python ACE/ExecutiveFunctionsLayer/app.py &> /dev/null &
# nohup python ACE/CognitiveControl/app.py &> /dev/null &
# nohup python ACE/TaskProsecution/app.py &> /dev/null &

# start the database server api in the systemApis folder
nohup python systemApis/app.py &> /dev/null &

# start the web interface for the system from the Frontend folder
nohup streamlit run Frontend/webInterface.py &> /dev/null &

# start the webspeech api in the webspeechModule folder
nohup python webspeechModule/app.py &> /dev/null &