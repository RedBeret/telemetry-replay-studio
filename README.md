# Telemetry Replay Studio

Telemetry Replay Studio is a full-stack analysis workspace for replaying runs, comparing sessions, scoring outcomes, and exporting clean debrief summaries.

The point of this project is to show a different side of the same engineering profile as `edge-lab-console`:

- time-series and event-driven data modeling
- replay and comparison workflows
- operator-facing debrief UX
- backend APIs that support analysis, not just CRUD
- product thinking for noisy technical systems

## Why This Project

This is designed to feel relevant to edge software, autonomy, platform, validation, and developer-tooling teams. Instead of another generic dashboard, it focuses on the moment after a run finishes:

1. What happened?
2. Where did behavior drift?
3. Which events actually mattered?
4. How do we hand off the result clearly?

## Current MVP

- Session list with health, score, and status
- Search and status filters for replay sessions
- Replay scrubber with frame-by-frame signal snapshots
- Timeline view with highlighted event windows
- Baseline comparison workflow with score deltas and focus areas
- Debrief export endpoint that produces a clean JSON handoff report
- Anomaly, artifact, and operator-note panels for session review

## Stack

- Frontend: React, TypeScript, Vite
- Backend: FastAPI
- Data: mocked structured telemetry payloads for the first iteration

## Local Development

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8010
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The Vite dev server proxies API traffic to `http://127.0.0.1:8010`.

## Verification

- `python -m unittest discover -s backend\tests -v`
- `python -m compileall backend\app`
- `npm run build`
