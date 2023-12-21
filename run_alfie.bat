@echo off

start cmd /k "title Aspirational Layer Support && call venv\Scripts\activate && python ACE\AspirationalLayer\GeminiSupport\GeminiSupport.py"
start cmd /k "title Global Strategy Layer Support && call venv\Scripts\activate && python ACE\GlobalStrategyLayer\GeminiSupport\GeminiSupport.py"
start cmd /k "title AgentModel Layer Support && call venv\Scripts\activate && python ACE\AgentModelLayer\GeminiSupport\GeminiSupport.py"
start cmd /k "title Executive Functions Layer Support && call venv\Scripts\activate && python ACE\ExecutiveFunctionsLayer\GeminiSupport\GeminiSupport.py"
start cmd /k "title Cognitive Control Support && call venv\Scripts\activate && python ACE\CognitiveControl\GeminiSupport\GeminiSupport.py"
start cmd /k "title Task Prosecution Support && call venv\Scripts\activate && python ACE\TaskProsecution\GeminiSupport\GeminiSupport.py"

start cmd /k "title Ochestration Unit && call venv\Scripts\activate && python ACE\OrchestrationUnit.py"
start cmd /k "title Web Interface && call venv\Scripts\activate && python webSpeechModule\app.py"