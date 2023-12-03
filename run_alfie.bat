@echo off

@REM Start all the layers of the system
@REM start cmd /k "call venv\Scripts\activate && python ACE\AspirationalLayer\app.py"
@REM start cmd /k "call venv\Scripts\activate && python ACE\GlobalStrategyLayer\app.py"
@REM start cmd /k "call venv\Scripts\activate && python ACE\AgentModelLayer\app.py"
@REM start cmd /k "call venv\Scripts\activate && python ACE\ExecutiveFunctionsLayer\app.py"
@REM start cmd /k "call venv\Scripts\activate && python ACE\CognitiveControl\app.py"
@REM start cmd /k "call venv\Scripts\activate && python ACE\TaskProsecution\app.py"


@REM Start all the layers of the system
start cmd /k "title Aspirational Layer && call venv\Scripts\activate && python ACE\AspirationalLayer\app.py"
start cmd /k "title Global Strategy Layer && call venv\Scripts\activate && python ACE\GlobalStrategyLayer\app.py"
start cmd /k "title AgentModel Layer && call venv\Scripts\activate && python ACE\AgentModelLayer\app.py"
@REM start cmd /k "title Layer 4 && call venv\Scripts\activate && python ACE\ExecutiveFunctionsLayer\app.py"
@REM start cmd /k "title Layer 5 && call venv\Scripts\activate && python ACE\CognitiveControl\app.py"
@REM start cmd /k "title Layer 6 && call venv\Scripts\activate && python ACE\TaskProsecution\app.py"

@REM start the database server api in the systemApis folder
start cmd /k "title Database Server && call venv\Scripts\activate && python systemApis\app.py"

@REM start the web interface for the system from the Frontend folder
start cmd /k "title Web Interface && call venv\Scripts\activate && streamlit run Frontend\webInterface.py"