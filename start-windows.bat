@echo off
cd /d "%~dp0"
where py >nul 2>&1
if %errorlevel%==0 (set PY=py) else (set PY=python)
%PY% -m pip install -r requirements.txt
%PY% -m uvicorn server:app --host 127.0.0.1 --port 8000
pause
