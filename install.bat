@echo off
REM Horizons Event Checker - One-Click Install & Run (Windows)
REM This script auto-installs Python, downloads the latest code, and runs it

echo ==================================
echo   Horizons Event Checker Setup
echo ==================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found. Downloading Python installer...
    
    REM Download Python installer
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.5/python-3.12.5-amd64.exe' -OutFile '%TEMP%\python-installer.exe'"
    
    echo Installing Python silently...
    echo Please wait...
    
    REM Install Python silently with PATH
    %TEMP%\python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1
    
    REM Refresh PATH
    set "PATH=%PATH%;%LOCALAPPDATA%\Programs\Python\Python312;%LOCALAPPDATA%\Programs\Python\Python312\Scripts"
    
    echo Python installed successfully!
) else (
    echo Python found:
    python --version
)

echo.
echo Downloading latest code from GitHub...
echo.

REM Download main.py from GitHub
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/QAISALNAJJAR/horizons-event-fix/main/main.py' -OutFile 'main.py'"

REM Download events.json from GitHub
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/QAISALNAJJAR/horizons-event-fix/main/events.json' -OutFile 'events.json'"

echo.
echo Installing required packages...
pip install requests browser-cookie3

echo.
echo ==================================
echo   Starting Horizons Event Checker
echo ==================================
echo.

python main.py

pause
