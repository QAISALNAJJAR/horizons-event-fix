@echo off
REM Horizons Event Checker - One-Click Install and Run (Windows)
REM This script downloads the pre-built executable or runs from source

echo ==================================
echo   Horizons Event Checker Setup
echo ==================================
echo.

set GITHUB_REPO=QAISALNAJJAR/horizons-event-fix
set PLATFORM=windows

REM Create temp directory
set TEMP_DIR=%TEMP%\horizons-checker
if not exist "%TEMP_DIR%" mkdir "%TEMP_DIR%"
cd /d "%TEMP_DIR%"

echo Downloading latest release...

REM Try to download pre-built binary
powershell -Command "try { Invoke-WebRequest -Uri 'https://github.com/%GITHUB_REPO%/releases/latest/download/horizons-checker-windows.exe' -OutFile 'horizons-checker.exe' -ErrorAction Stop; exit 0 } catch { exit 1 }"

if exist horizons-checker.exe (
    echo Downloaded pre-built binary!
    echo.
    echo ==================================
    echo   Starting Horizons Event Checker
    echo ==================================
    echo.
    horizons-checker.exe
    goto :cleanup
)

echo Pre-built binary not found. Downloading source and building...

REM Download source files
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/%GITHUB_REPO%/main/main.py' -OutFile 'main.py'"
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/%GITHUB_REPO%/main/events.json' -OutFile 'events.json'"
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/%GITHUB_REPO%/main/requirements.txt' -OutFile 'requirements.txt'"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found. Downloading Python installer...
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.5/python-3.12.5-amd64.exe' -OutFile '%TEMP%\python-installer.exe'"
    echo Installing Python silently...
    %TEMP%\python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1
    set "PATH=%PATH%;%LOCALAPPDATA%\Programs\Python\Python312;%LOCALAPPDATA%\Programs\Python\Python312\Scripts"
)

REM Install dependencies and run
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo ==================================
echo   Starting Horizons Event Checker
echo ==================================
echo.

python main.py

:cleanup
cd /d %TEMP%
rd /s /q "%TEMP_DIR%" 2>nul

pause
