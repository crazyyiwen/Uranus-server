@echo off
echo Starting Uranus Server...
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the server
python main.py
