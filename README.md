# Telemetry Replay Studio

Telemetry Replay Studio is a post-run analysis workspace for edge and autonomy teams. A run finishes, you open the debrief, you need to know what happened and why, and you need to hand the result off cleanly. This is the tool for that moment.

This is distinct from `edge-lab-console`. Edge-lab-console handles run configuration and execution. Telemetry Replay Studio handles what comes after: replay, drift detection, scoring, and team-ready handoff summaries.

## What you do here

- Load a replay session and scrub through it frame by frame
- See where behavior diverged from a baseline
- Get a score that tells you at a glance whether the run is clean, degraded, or anomalous
- Flag anomalies and artifacts during review
- Export a debrief summary that a teammate can read without having the session open

## Scoring rubric

Scores are 0-100. The scale is not decorative.

| Score | Meaning |
|-------|---------|
| 90-100 | Run is within tolerance. Minor deviations only. Safe to proceed. |
| 70-89  | Minor degradation. Review flagged events before handoff. |
| 50-69  | Meaningful drift detected. Events require explanation before proceed. |
| 30-49  | Significant anomalies. Run likely needs a retry. |
| 0-29   | Critical failure. Do not proceed until root cause is identified and resolved. |

### What gets flagged automatically

- Any metric that exceeds its baseline threshold by more than 2 standard deviations
- Missing telemetry frames (gaps in the signal)
- Out-of-order event sequencing
- Any operator-annotated anomaly: artifact, inconsistency, or unusual pattern

Operator annotations carry weight. They can push a borderline score lower even if automatic metrics are nominal. This is intentional.

## Comparison workflow

Select a baseline session, then run a comparison against the current session.

Baseline run, nominal:

```
Score: 94
Health: NOMINAL
Flags: 0
Top events: [steer_correction @ 14.2s, sensor_fusion_recovery @ 31.7s]
```

Current run, same config, later date:

```
Score: 61
Health: DEGRADED
Delta: -33 points

Flags:
  - sensor_lag @ 9.1s (exceeded 2sigma threshold)
  - gap_detected @ 22.4s (missing telemetry frame)
  - steer_overshoot @ 47.2s (out-of-sequence)

Top drift window: 18.0s - 35.0s
Root cause suspect: sensor fusion pipeline on reinitialization
```

That delta is the product. You see the gap, the window where it opened, and what to look at first.

## Features

- Session list with health, score, and status filters
- Frame-by-frame replay scrubber with signal snapshots
- Timeline view with highlighted event windows
- Baseline comparison with delta scoring and focus area isolation
- Debrief export: clean JSON handoff report with scores, flags, and annotations
- Anomaly panel, artifact panel, and operator notes per session

## Local Development

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8010
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Vite proxies API traffic to `http://127.0.0.1:8010`.

## Verification

```bash
python -m unittest discover -s backend/tests -v
python -m compileall backend/app
npm run build
```
