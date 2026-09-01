@echo off
REM Horizons Event Checker - Simple Runner (No Admin Required)
REM Runs the latest version without admin privileges

echo ==================================
echo   Horizons Event Checker
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

echo Python found:
python --version
echo.

echo Downloading latest code...

REM Download files
powershell -Command "try { Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/%GITHUB_REPO%/main/main.py' -OutFile 'main.py' } catch { echo Failed to download!; pause; goto :cleanup }"
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

:cleanup
echo.
echo Press any key to exit...
pause

REM Cleanup
cd /d %TEMP%
rd /s /q "%TEMP_DIR%" 2>nul
