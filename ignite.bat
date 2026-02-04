@echo off
title REALM FORGE SOVEREIGN IGNITION
echo 🌀 Preparing Industrial Package Structure...

:: Recursively create __init__.py files where missing
for /r "src" %%d in (.) do (
    if not exist "%%d\__init__.py" (
        echo. > "%%d\__init__.py"
    )
)

echo ✅ Package Structure Regulated.
echo 🔍 Running Workforce Validator...
python -m src.orchestration.validator

echo 🚀 Starting Sovereign Gateway...
:: Note: Using src.app:app because our root is F:\agentic_workforce
uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload
pause