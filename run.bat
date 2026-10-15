@echo off
REM Telemetry Replay Studio — start both services
REM Run from the repo root. Two terminal windows will open.

echo Starting backend...
start "TRS Backend" cmd /k "cd backend && python -m venv .venv && .venv\Scripts\activate && pip install -r requirements.txt && uvicorn app.main:app --reload --port 8010"

echo Starting frontend...
start "TRS Frontend" cmd /k "cd frontend && npm install && npm run dev"

echo.
echo Backend:  http://127.0.0.1:8010
echo Frontend: http://localhost:5173
echo.
echo Close the two terminal windows to stop both services.
