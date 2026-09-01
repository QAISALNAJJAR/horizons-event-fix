@echo off
REM Horizons Event Checker - Windows Installer
REM Downloads and runs the latest version

echo ==================================
echo   Horizons Event Checker Setup
echo ==================================
echo.

set GITHUB_REPO=QAISALNAJJAR/horizons-event-fix

REM Create temp directory
set TEMP_DIR=%TEMP%\horizons-checker
if not exist "%TEMP_DIR%" mkdir "%TEMP_DIR%"
cd /d "%TEMP_DIR%"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found. Installing automatically...
    echo.
    
    REM Download Python installer
    echo Downloading Python...
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.5/python-3.12.5-amd64.exe' -OutFile '%TEMP%\python-installer.exe'"
    
    REM Install Python silently with PATH enabled
    echo Installing Python (this may take a few minutes)...
    %TEMP%\python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1
    
    REM Refresh PATH for current session
    set "PATH=%PATH%;%LOCALAPPDATA%\Programs\Python\Python312;%LOCALAPPDATA%\Programs\Python\Python312\Scripts;%ProgramFiles%\Python312;%ProgramFiles%\Python312\Scripts"
    
    echo Python installed successfully!
    echo.
) else (
    echo Python found:
    python --version
)

echo Downloading latest code...

REM Download files
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/%GITHUB_REPO%/main/main.py' -OutFile 'main.py'"
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/%GITHUB_REPO%/main/events.json' -OutFile 'events.json'"
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/%GITHUB_REPO%/main/requirements.txt' -OutFile 'requirements.txt'"

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo ==================================
echo   Starting Horizons Event Checker
echo ==================================
echo.

python main.py

REM Cleanup
cd /d %TEMP%
rd /s /q "%TEMP_DIR%" 2>nul

pause
