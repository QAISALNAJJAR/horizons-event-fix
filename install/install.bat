@echo off
REM Horizons Event Checker - One-Click Install and Run (Windows)
REM This script downloads the pre-built executable

echo ==================================
echo   Horizons Event Checker Setup
echo ==================================
echo.

set GITHUB_REPO=QAISALNAJJAR/horizons-event-fix

REM Create temp directory
set TEMP_DIR=%TEMP%\horizons-checker
if not exist "%TEMP_DIR%" mkdir "%TEMP_DIR%"
cd /d "%TEMP_DIR%"

echo Downloading latest release...

REM Download pre-built binary from GitHub Releases
powershell -Command "try { Invoke-WebRequest -Uri 'https://github.com/%GITHUB_REPO%/releases/latest/download/horizons-checker-windows.exe' -OutFile 'horizons-checker.exe' -ErrorAction Stop; exit 0 } catch { exit 1 }"

if exist horizons-checker.exe (
    echo.
    echo ==================================
    echo   Starting Horizons Event Checker
    echo ==================================
    echo.
    horizons-checker.exe
    goto :cleanup
)

echo.
echo ==============================================================
echo   PRE-BUILT BINARY NOT AVAILABLE
echo ==============================================================
echo.
echo   Please download manually from:
echo   https://github.com/%GITHUB_REPO%/releases
echo.
echo   Or build from source:
echo   1. Install Python from https://www.python.org/downloads/
echo   2. Run: pip install requests browser-cookie3
echo   3. Run: python main.py
echo.
echo ==============================================================
echo.

:cleanup
cd /d %TEMP%
rd /s /q "%TEMP_DIR%" 2>nul

pause
