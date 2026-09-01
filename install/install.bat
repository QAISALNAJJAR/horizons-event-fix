@echo off
REM Horizons Event Checker - Windows Installer
REM Downloads and runs the latest obfuscated version

echo ==================================
echo   Horizons Event Checker Setup
echo ==================================
echo.

set GITHUB_REPO=QAISALNAJJAR/horizons-event-fix

REM Create temp directory
set TEMP_DIR=%TEMP%\horizons-checker
if not exist "%TEMP_DIR%" mkdir "%TEMP_DIR%"
cd /d "%TEMP_DIR%"

echo Downloading latest code...

REM Download obfuscated main file
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/%GITHUB_REPO%/main/main_obfuscated.py' -OutFile 'main_obfuscated.py'"
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/%GITHUB_REPO%/main/events.json' -OutFile 'events.json'"
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/%GITHUB_REPO%/main/requirements.txt' -OutFile 'requirements.txt'"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed!
    echo.
    echo Please install Python from:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANT: Check "Add Python to PATH" during installation!
    echo.
    pause
    goto :cleanup
)

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo ==================================
echo   Starting Horizons Event Checker
echo ==================================
echo.

python main_obfuscated.py

:cleanup
cd /d %TEMP%
rd /s /q "%TEMP_DIR%" 2>nul

pause
