@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    if exist "%LocalAppData%\Programs\Python\Python313\python.exe" (
        "%LocalAppData%\Programs\Python\Python313\python.exe" -m venv .venv
    ) else (
        py -3 -m venv .venv
    )
    if errorlevel 1 goto echec
)
set "PY=.venv\Scripts\python.exe"
"%PY%" -c "import flask" >nul 2>&1
if errorlevel 1 (
    "%PY%" -m pip install -r requirements.txt
    if errorlevel 1 goto echec
)
"%PY%" creer_db.py >nul
if errorlevel 1 goto echec
echo Ouvre http://127.0.0.1:5000 dans ton navigateur. Ctrl+C pour arreter.
"%PY%" -m flask --app app run --host 127.0.0.1 --port 5000
if errorlevel 1 goto echec
exit /b 0
:echec
echo Le lancement a echoue. Consulte le message ci-dessus.
pause
exit /b 1
