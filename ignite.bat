@echo off
title REALM FORGE SOVEREIGN IGNITION
echo 🌀 Preparing Industrial Package Structure...

:: This PowerShell command ensures every folder has an __init__.py
powershell -Command "Get-ChildItem -Path 'src' -Recurse -Directory | ForEach-Object { if (!(Test-Path \"$($_.FullName)\__init__.py\")) { New-Item -Path \"$($_.FullName)\__init__.py\" -ItemType 'file' } }"

echo ✅ Package Structure Regulated.
echo 🔍 Running Workforce Validator...
python -m src.orchestration.validator

echo 🚀 Starting Sovereign Gateway...
uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload
pause