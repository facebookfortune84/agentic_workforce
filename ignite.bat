@echo off
title REALM FORGE IGNITION
echo 🌀 Awakening Sovereign System...

:: 1. Generate Missing __init__ files
for /r "src" %%d in (.) do (
    if not exist "%%d\__init__.py" type nul > "%%d\__init__.py"
)

:: 2. Run Industrial Validator
echo 🔍 Auditing 1,100+ Agent Manifests...
python -m src.orchestration.validator

:: 3. Launch Backend
echo 🚀 Igniting Sovereign Gateway on Port 8000...
start cmd /k "uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload"

:: 4. Launch Tunnel (Ngrok)
echo 🌀 Start your ngrok tunnel in a new window: ngrok http 8000
echo ✅ System is live.
pause