@echo off
REM Horizons Event Checker - Windows Installer

echo Starting... > "%TEMP%\horizons.log" 2>&1

REM Check admin
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if '%errorlevel%' NEQ '0' (
    echo NOT ADMIN >> "%TEMP%\horizons.log" 2>&1
    echo.
    echo PLEASE RUN AS ADMINISTRATOR
    echo Right-click -^> Run as administrator
    echo.
    pause
    exit /B
)

echo IS ADMIN >> "%TEMP%\horizons.log" 2>&1

set TEMP_DIR=%TEMP%\horizons-checker
if not exist "%TEMP_DIR%" mkdir "%TEMP_DIR%"
cd /d "%TEMP_DIR%"

echo DIR: %TEMP_DIR% >> "%TEMP%\horizons.log" 2>&1

REM Check Python
python --version >> "%TEMP%\horizons.log" 2>&1
if errorlevel 1 (
    echo Python not found! >> "%TEMP%\horizons.log" 2>&1
    echo.
    echo Python not found. Downloading...
    
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.5/python-3.12.5-amd64.exe' -OutFile '%TEMP%\python.exe'"
    %TEMP%\python.exe /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1
    
    python --version >> "%TEMP%\horizons.log" 2>&1
    if errorlevel 1 (
        echo Python install failed! >> "%TEMP%\horizons.log" 2>&1
        echo Failed to install Python!
        pause
        goto :cleanup
    )
)

echo Downloading code... >> "%TEMP%\horizons.log" 2>&1
echo.
echo Downloading latest code...

powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/QAISALNAJJAR/horizons-event-fix/main/main.py' -OutFile 'main.py'"
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/QAISALNAJJAR/horizons-event-fix/main/events.json' -OutFile 'events.json'"
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/QAISALNAJJAR/horizons-event-fix/main/requirements.txt' -OutFile 'requirements.txt'"

echo Installing dependencies...
echo Installing deps... >> "%TEMP%\horizons.log" 2>&1
pip install -r requirements.txt

echo.
echo Starting Horizons Event Checker...
echo.
python main.py

:cleanup
echo.
echo Done. Check log: %TEMP%\horizons.log
pause
