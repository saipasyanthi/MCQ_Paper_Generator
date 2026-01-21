@echo off
REM Startup script for MCQ Paper Generator Web App (Windows)

echo ======================================================
echo     MCQ PAPER GENERATOR - WEB APPLICATION
echo ======================================================
echo.

REM Activate virtual environment if it exists
if exist ".venv" (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
)

REM Install dependencies if needed
python -c "import flask" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install flask werkzeug
)

REM Start the web server
echo.
echo Starting web server...
echo.
python app_web.py
pause
