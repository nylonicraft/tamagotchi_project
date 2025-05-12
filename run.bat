@echo off

start uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000

timeout /t 3 >nul

start http://127.0.0.1:8000