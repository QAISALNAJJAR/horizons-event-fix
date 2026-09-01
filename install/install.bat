@echo off
REM Horizons Event Checker - Windows Installer
REM Downloads and runs the latest version

REM Log output for debugging
echo Starting installer... > "%TEMP%\horizons-install.log"
date /t >> "%TEMP%\horizons-install.log"
time /t >> "%TEMP%\horizons-install.log"

REM Check if running as admin
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if '%errorlevel%' NEQ '0' (
    echo.
    echo ==============================================================
    echo   PLEASE RUN AS ADMINISTRATOR
    echo ==============================================================
    echo.
    echo   Right-click this file and select "Run as administrator"
    echo.
    echo ==============================================================
    echo.
    pause
    exit /B
)

echo Running as administrator... >> "%TEMP%\horizons-install.log"

set GITHUB_REPO=QAISALNAJJAR/horizons-event-fix

REM Create temp directory
set TEMP_DIR=%TEMP%\horizons-checker
if not exist "%TEMP_DIR%" mkdir "%TEMP_DIR%"
cd /d "%TEMP_DIR%"

echo Working directory: %TEMP_DIR% >> "%TEMP%\horizons-install.log"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found. Installing automatically...
    echo.
    
    REM Download Python installer
    echo Downloading Python...
    echo Downloading Python installer... >> "%TEMP%\horizons-install.log"
    powershell -Command "try { Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/pymanager/python-manager-26.3.msix' -OutFile '%TEMP%\python-manager.msix'; echo Download success >> '%TEMP%\horizons-install.log' } catch { echo Download failed >> '%TEMP%\horizons-install.log'; exit 1 }"
    
    REM Try to install Python silently
    echo Installing Python (this may take a few minutes)...
    echo Installing Python... >> "%TEMP%\horizons-install.log"
    powershell -Command "Add-AppxPackage -Path '%TEMP%\python-manager.msix'"
    
    REM Check if installation succeeded
    python --version >nul 2>&1
    if errorlevel 1 (
        echo.
        echo ==============================================================
        echo   AUTO-INSTALL FAILED
        echo ==============================================================
        echo.
        echo   Please install Python manually:
        echo   1. Open this file: %TEMP%\python-manager.msix
        echo   2. Follow the installation wizard
        echo   3. Re-run this installer
        echo.
        echo   Or download from: https://www.python.org/downloads/
        echo.
        echo ==============================================================
        echo.
        pause
        goto :cleanup
    )
    
    echo Python installed successfully!
    echo.
) else (
    echo Python found:
    python --version
)

echo Downloading latest code...

REM Download files
powershell -Command "try { Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/%GITHUB_REPO%/main/main.py' -OutFile 'main.py' } catch { echo Failed to download main.py!; pause; goto :cleanup }"
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
