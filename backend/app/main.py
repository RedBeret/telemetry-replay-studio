from __future__ import annotations

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .mock_data import get_debrief_report
from .mock_data import get_replay_catalog
from .mock_data import get_session_comparison
from .mock_data import get_session_detail

app = FastAPI(title="Telemetry Replay Studio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/replay")
def replay_data() -> dict:
    return get_replay_catalog()


@app.get("/api/replay/{session_id}")
def replay_session(session_id: str) -> dict:
    try:
        return get_session_detail(session_id)
    except KeyError as error:
        raise HTTPException(status_code=404, detail="Session not found") from error


@app.get("/api/replay/{session_id}/compare/{baseline_id}")
def replay_comparison(session_id: str, baseline_id: str) -> dict:
    try:
        return get_session_comparison(session_id, baseline_id)
    except KeyError as error:
        raise HTTPException(status_code=404, detail="Comparison not found") from error


@app.get("/api/replay/{session_id}/debrief")
def replay_debrief(session_id: str, baseline_id: str | None = None) -> dict:
    try:
        return get_debrief_report(session_id, baseline_id)
    except KeyError as error:
        raise HTTPException(status_code=404, detail="Debrief source not found") from error
