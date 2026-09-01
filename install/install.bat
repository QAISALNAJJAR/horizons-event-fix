@echo off
REM Horizons Event Checker - Windows Installer
REM Downloads and runs the latest version

REM Force run as administrator
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    if exist "%temp%\getadmin.vbs" ( del "%temp%\getadmin.vbs" )
    pushd "%CD%"
    CD /D "%~dp0"

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
    powershell -Command "try { Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/pymanager/python-manager-26.3.msix' -OutFile '%TEMP%\python-manager.msix' } catch { echo Download failed!; exit 1 }"
    
    REM Try to install Python silently
    echo Installing Python (this may take a few minutes)...
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
powershell -Command "try { Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/%GITHUB_REPO%/main/main.py' -OutFile 'main.py' } catch { echo Failed to download main.py!; exit 1 }"
powershell -Command "try { Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/%GITHUB_REPO%/main/events.json' -OutFile 'events.json' } catch { echo Failed to download events.json!; exit 1 }"
powershell -Command "try { Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/%GITHUB_REPO%/main/requirements.txt' -OutFile 'requirements.txt' } catch { echo Failed to download requirements.txt!; exit 1 }"

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo Failed to install dependencies!
    pause
    goto :cleanup
)

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
