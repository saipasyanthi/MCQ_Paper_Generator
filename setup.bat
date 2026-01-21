@echo off
REM Setup script for MCQ Paper Generator (Windows)
REM Run: setup.bat

echo ==================================
echo MCQ Paper Generator
echo Setup Script - Windows
echo ==================================
echo.

REM Check Python
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found
    echo Please install Python 3.7+ from python.org
    pause
    exit /b 1
)

python --version
echo OK - Python found
echo.

REM Check pip
echo [2/5] Checking pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo Installing pip...
    python -m ensurepip --default-pip
)
echo OK - Pip available
echo.

REM Install dependencies
echo [3/5] Installing dependencies...
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo Error installing dependencies
    pause
    exit /b 1
)

echo OK - Dependencies installed
echo.

REM Create directories
echo [4/5] Setting up directories...
if not exist output mkdir output
if not exist licenses mkdir licenses
echo OK - Directories created
echo.

REM License setup
echo [5/5] License Setup
echo.
echo Would you like to:
echo 1. Generate a new license (for administrator)
echo 2. Skip (if you already have license.json)
set /p choice="Choose (1 or 2): "

if "%choice%"=="1" (
    echo.
    python license_generator.py
)

echo.
echo ==================================
echo OK - Setup Complete!
echo ==================================
echo.
echo To start the application, run:
echo   python app.py
echo.
echo For more information, see README_GUI.md
echo.
pause
