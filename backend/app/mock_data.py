from __future__ import annotations

from copy import deepcopy
from statistics import mean
from typing import Any


SESSIONS: list[dict[str, Any]] = [
    {
        "id": "TRS-3101",
        "title": "Jetson Vision Stack Replay",
        "status": "review",
        "score": 91,
        "durationSeconds": 1480,
        "environment": "lab-a",
        "vehicle": "bench-12",
        "missionProfile": "vision-stack-burn-in",
        "summary": "Stable inference throughout most of the run with a late spike in latency after a sensor reset event.",
        "anomalies": 3,
    },
    {
        "id": "TRS-3102",
        "title": "Autonomy Regression Sweep",
        "status": "flagged",
        "score": 74,
        "durationSeconds": 1725,
        "environment": "sim-west",
        "vehicle": "sim-node-7",
        "missionProfile": "route-regression-17b",
        "summary": "Confidence recovered after retry, but route-tracking drift exceeded baseline tolerance during the second leg.",
        "anomalies": 5,
    },
    {
        "id": "TRS-3103",
        "title": "Telemetry Uplink Endurance",
        "status": "passed",
        "score": 96,
        "durationSeconds": 1320,
        "environment": "field-east",
        "vehicle": "relay-03",
        "missionProfile": "uplink-endurance",
        "summary": "Healthy uplink performance and clean reconnect behavior after a planned link drop.",
        "anomalies": 1,
    },
]


SESSION_DETAILS: dict[str, dict[str, Any]] = {
    "TRS-3101": {
        "id": "TRS-3101",
        "title": "Jetson Vision Stack Replay",
        "status": "review",
        "score": 91,
        "summary": "Replay shows clean inference cadence for most of the mission, with a short but visible latency spike after a camera service reset.",
        "verdict": "Good candidate for promotion after confirming the reset window remains bounded.",
        "compareCandidates": [
            {"id": "TRS-3094", "title": "Vision Stack Baseline", "score": 94},
            {"id": "TRS-3088", "title": "Camera Failover Soak", "score": 89},
        ],
        "metrics": [
            {"label": "Inference Accuracy", "value": "94.6%", "delta": "-1.1%", "trend": "down"},
            {"label": "Avg. Frame Latency", "value": "88 ms", "delta": "+11 ms", "trend": "up"},
            {"label": "Reset Recovery Time", "value": "2.7 s", "delta": "+0.3 s", "trend": "up"},
        ],
        "signalFrames": [
            {"time": "00:00", "accuracy": 97, "latency": 62, "linkQuality": 96, "confidence": 95, "note": "Mission initialization complete."},
            {"time": "03:10", "accuracy": 95, "latency": 75, "linkQuality": 94, "confidence": 94, "note": "Stable tracking through the first target pass."},
            {"time": "06:42", "accuracy": 94, "latency": 118, "linkQuality": 93, "confidence": 89, "note": "Camera service reset triggered a visible latency surge."},
            {"time": "11:25", "accuracy": 95, "latency": 82, "linkQuality": 95, "confidence": 93, "note": "System recovered within acceptable bounds."},
        ],
        "timeline": [
            {"time": "00:00", "type": "info", "title": "Replay initialized", "detail": "Vision pipeline loaded with baseline profile 6A."},
            {"time": "06:31", "type": "warning", "title": "Camera service reset", "detail": "Primary vision service restarted after dropping two frames."},
            {"time": "06:42", "type": "warning", "title": "Latency surge", "detail": "Latency peaked at 118 ms during warm-up after reset."},
            {"time": "08:15", "type": "success", "title": "Confidence normalized", "detail": "Accuracy and latency returned close to baseline after stabilization."},
        ],
        "anomalies": [
            {"severity": "medium", "window": "06:31 - 06:54", "title": "Reset-related latency spike", "owner": "Vision services"},
            {"severity": "low", "window": "02:18 - 02:41", "title": "Minor frame drop cluster", "owner": "Capture pipeline"},
            {"severity": "low", "window": "10:02 - 10:22", "title": "Short confidence wobble", "owner": "Detection model"},
        ],
        "artifacts": [
            {"name": "vision-stack-replay.json", "kind": "summary"},
            {"name": "camera-reset-window.mp4", "kind": "clip"},
            {"name": "latency-heatmap-3101.csv", "kind": "telemetry"},
        ],
        "notes": [
            {"author": "Steven", "time": "Apr 12, 08:18 AM", "text": "The reset window is visible but contained. Worth watching if ambient load increases."},
            {"author": "Validation", "time": "Apr 12, 08:32 AM", "text": "No operator-visible impact after recovery. Keep as watch item, not blocker."},
        ],
    },
    "TRS-3102": {
        "id": "TRS-3102",
        "title": "Autonomy Regression Sweep",
        "status": "flagged",
        "score": 74,
        "summary": "Replay shows a clean first leg, a drift event after route replanning, and a recovery sequence that completed with reduced confidence.",
        "verdict": "Investigate before promotion. Route drift exceeded corridor tolerance during the replan window.",
        "compareCandidates": [
            {"id": "TRS-3098", "title": "Clean baseline for route profile 17B", "score": 93},
            {"id": "TRS-3085", "title": "Crosswind stress run", "score": 81},
            {"id": "TRS-3079", "title": "Previous regression candidate", "score": 77},
        ],
        "metrics": [
            {"label": "Route Accuracy", "value": "87%", "delta": "-9%", "trend": "down"},
            {"label": "Avg. Decision Latency", "value": "122 ms", "delta": "+18 ms", "trend": "up"},
            {"label": "Reconnect Time", "value": "4.2 s", "delta": "+0.6 s", "trend": "up"},
        ],
        "signalFrames": [
            {"time": "00:00", "accuracy": 96, "latency": 74, "linkQuality": 95, "confidence": 95, "note": "Mission loaded with baseline route profile 17B."},
            {"time": "04:12", "accuracy": 91, "latency": 89, "linkQuality": 93, "confidence": 82, "note": "Camera confidence dipped before the route replan."},
            {"time": "09:41", "accuracy": 83, "latency": 131, "linkQuality": 90, "confidence": 71, "note": "Largest drift window started after replanning event."},
            {"time": "12:02", "accuracy": 85, "latency": 126, "linkQuality": 88, "confidence": 75, "note": "Retry recovered heading but convergence remained slow."},
            {"time": "14:18", "accuracy": 88, "latency": 118, "linkQuality": 91, "confidence": 80, "note": "Recovery confirmed, but final stability stayed below baseline."},
        ],
        "timeline": [
            {"time": "00:00", "type": "info", "title": "Replay initialized", "detail": "Mission profile loaded with baseline route profile 17B."},
            {"time": "04:12", "type": "warning", "title": "Sensor confidence dip", "detail": "Camera confidence dropped below expected tolerance for 18 seconds."},
            {"time": "09:41", "type": "critical", "title": "Route drift detected", "detail": "Trajectory deviated 6.8m outside baseline corridor after replanning event."},
            {"time": "12:02", "type": "warning", "title": "Retry convergence slow", "detail": "Recovery logic reacquired the path with slower-than-baseline steering response."},
            {"time": "14:18", "type": "success", "title": "Recovery confirmed", "detail": "Pathing stabilized after retry with reduced but acceptable confidence."},
        ],
        "anomalies": [
            {"severity": "high", "window": "09:41 - 10:08", "title": "Route drift outside tolerance", "owner": "Autonomy planning"},
            {"severity": "medium", "window": "04:12 - 04:30", "title": "Vision confidence dip", "owner": "Perception"},
            {"severity": "medium", "window": "11:58 - 12:20", "title": "Slow retry convergence", "owner": "Recovery logic"},
            {"severity": "low", "window": "07:10 - 07:30", "title": "Minor link jitter", "owner": "Telemetry"},
            {"severity": "low", "window": "13:21 - 13:44", "title": "Short heading oscillation", "owner": "Control loop"},
        ],
        "artifacts": [
            {"name": "run-3102-summary.json", "kind": "summary"},
            {"name": "route-diff-3102.csv", "kind": "comparison"},
            {"name": "camera-confidence-window.mp4", "kind": "clip"},
        ],
        "notes": [
            {"author": "Steven", "time": "Apr 12, 09:40 AM", "text": "Route drift appears tied to the replan window, not the initial mission profile."},
            {"author": "Ops Lead", "time": "Apr 12, 09:56 AM", "text": "Worth checking this against the prior clean baseline before raising a blocker."},
            {"author": "Autonomy", "time": "Apr 12, 10:14 AM", "text": "Could be interaction between the crosswind patch and the retry threshold."},
        ],
    },
    "TRS-3103": {
        "id": "TRS-3103",
        "title": "Telemetry Uplink Endurance",
        "status": "passed",
        "score": 96,
        "summary": "Replay confirms healthy reconnect behavior and clean link-quality recovery after a planned uplink interruption.",
        "verdict": "Ready for promotion. Link handling stayed within margin across the full endurance window.",
        "compareCandidates": [
            {"id": "TRS-3090", "title": "Prior endurance baseline", "score": 95},
            {"id": "TRS-3081", "title": "Degraded comms shakeout", "score": 88},
        ],
        "metrics": [
            {"label": "Avg. Link Quality", "value": "94%", "delta": "+2%", "trend": "up"},
            {"label": "Reconnect Time", "value": "2.1 s", "delta": "-0.7 s", "trend": "down"},
            {"label": "Packet Loss", "value": "0.8%", "delta": "-1.3%", "trend": "down"},
        ],
        "signalFrames": [
            {"time": "00:00", "accuracy": 95, "latency": 58, "linkQuality": 96, "confidence": 95, "note": "Endurance run began with a healthy uplink."},
            {"time": "05:14", "accuracy": 94, "latency": 61, "linkQuality": 48, "confidence": 91, "note": "Planned comms interruption triggered reconnect path."},
            {"time": "05:17", "accuracy": 95, "latency": 69, "linkQuality": 82, "confidence": 93, "note": "Recovery was clean within the expected retry window."},
            {"time": "11:45", "accuracy": 96, "latency": 57, "linkQuality": 95, "confidence": 96, "note": "Run finished with stable uplink health."},
        ],
        "timeline": [
            {"time": "00:00", "type": "info", "title": "Replay initialized", "detail": "Telemetry endurance profile loaded with reconnect threshold 3.0 seconds."},
            {"time": "05:14", "type": "warning", "title": "Planned link interruption", "detail": "Uplink was intentionally dropped to verify reconnect behavior."},
            {"time": "05:17", "type": "success", "title": "Reconnect completed", "detail": "Client rejoined and flushed queued telemetry in 2.1 seconds."},
            {"time": "11:45", "type": "success", "title": "Endurance run complete", "detail": "No unexpected dropouts after the planned outage window."},
        ],
        "anomalies": [
            {"severity": "low", "window": "05:14 - 05:17", "title": "Expected reconnect event", "owner": "Telemetry"},
        ],
        "artifacts": [
            {"name": "uplink-endurance-report.json", "kind": "summary"},
            {"name": "reconnect-window.csv", "kind": "telemetry"},
            {"name": "queue-flush-report.txt", "kind": "notes"},
        ],
        "notes": [
            {"author": "Steven", "time": "Apr 12, 11:55 AM", "text": "Cleanest reconnect window in the last three endurance runs."},
            {"author": "QA", "time": "Apr 12, 12:02 PM", "text": "No follow-up needed before promotion to the next soak stage."},
        ],
    },
}


COMPARISONS: dict[str, dict[str, dict[str, Any]]] = {
    "TRS-3101": {
        "TRS-3094": {
            "baselineId": "TRS-3094",
            "baselineTitle": "Vision Stack Baseline",
            "summary": "Most metrics are close to baseline. The visible delta is concentrated inside the camera reset window.",
            "scoreDelta": -3,
            "largestWindow": "06:31 - 06:54",
            "recommendation": "Monitor in the next burn-in cycle, but no release stop is suggested.",
            "focusAreas": [
                {"label": "Latency", "current": "88 ms", "baseline": "77 ms", "delta": "+11 ms"},
                {"label": "Recovery", "current": "2.7 s", "baseline": "2.4 s", "delta": "+0.3 s"},
                {"label": "Accuracy", "current": "94.6%", "baseline": "95.7%", "delta": "-1.1%"},
            ],
        },
        "TRS-3088": {
            "baselineId": "TRS-3088",
            "baselineTitle": "Camera Failover Soak",
            "summary": "Compared with a harsher failover profile, this run recovered faster and held accuracy better through reset.",
            "scoreDelta": 2,
            "largestWindow": "06:31 - 06:54",
            "recommendation": "Performance is acceptable relative to the failover stress profile.",
            "focusAreas": [
                {"label": "Latency", "current": "88 ms", "baseline": "96 ms", "delta": "-8 ms"},
                {"label": "Recovery", "current": "2.7 s", "baseline": "3.1 s", "delta": "-0.4 s"},
                {"label": "Accuracy", "current": "94.6%", "baseline": "93.8%", "delta": "+0.8%"},
            ],
        },
    },
    "TRS-3102": {
        "TRS-3098": {
            "baselineId": "TRS-3098",
            "baselineTitle": "Clean baseline for route profile 17B",
            "summary": "The replay diverged hardest during the replan window, where route adherence dropped and steering took longer to settle.",
            "scoreDelta": -19,
            "largestWindow": "09:41 - 10:08",
            "recommendation": "Block promotion until the replan logic and retry threshold are checked together.",
            "focusAreas": [
                {"label": "Route Accuracy", "current": "87%", "baseline": "96%", "delta": "-9%"},
                {"label": "Decision Latency", "current": "122 ms", "baseline": "104 ms", "delta": "+18 ms"},
                {"label": "Reconnect Time", "current": "4.2 s", "baseline": "3.6 s", "delta": "+0.6 s"},
            ],
        },
        "TRS-3085": {
            "baselineId": "TRS-3085",
            "baselineTitle": "Crosswind stress run",
            "summary": "This run still drifted more than expected, but it outperformed the crosswind stress scenario in overall stability.",
            "scoreDelta": -7,
            "largestWindow": "09:41 - 10:08",
            "recommendation": "Use this comparison to narrow whether the regression is route-specific or environment-specific.",
            "focusAreas": [
                {"label": "Route Accuracy", "current": "87%", "baseline": "81%", "delta": "+6%"},
                {"label": "Decision Latency", "current": "122 ms", "baseline": "129 ms", "delta": "-7 ms"},
                {"label": "Reconnect Time", "current": "4.2 s", "baseline": "4.4 s", "delta": "-0.2 s"},
            ],
        },
        "TRS-3079": {
            "baselineId": "TRS-3079",
            "baselineTitle": "Previous regression candidate",
            "summary": "The regression signature is similar to the prior candidate, but the new run recovers earlier and ends in a better state.",
            "scoreDelta": -3,
            "largestWindow": "09:41 - 10:08",
            "recommendation": "Useful for validating that the recent patch improved recovery without fully fixing the root cause.",
            "focusAreas": [
                {"label": "Route Accuracy", "current": "87%", "baseline": "84%", "delta": "+3%"},
                {"label": "Decision Latency", "current": "122 ms", "baseline": "126 ms", "delta": "-4 ms"},
                {"label": "Reconnect Time", "current": "4.2 s", "baseline": "4.5 s", "delta": "-0.3 s"},
            ],
        },
    },
    "TRS-3103": {
        "TRS-3090": {
            "baselineId": "TRS-3090",
            "baselineTitle": "Prior endurance baseline",
            "summary": "Reconnect timing and packet-loss handling both improved compared with the previous endurance baseline.",
            "scoreDelta": 1,
            "largestWindow": "05:14 - 05:17",
            "recommendation": "Promotion is reasonable. Keep the new retry settings as the working baseline.",
            "focusAreas": [
                {"label": "Link Quality", "current": "94%", "baseline": "92%", "delta": "+2%"},
                {"label": "Reconnect Time", "current": "2.1 s", "baseline": "2.8 s", "delta": "-0.7 s"},
                {"label": "Packet Loss", "current": "0.8%", "baseline": "2.1%", "delta": "-1.3%"},
            ],
        },
        "TRS-3081": {
            "baselineId": "TRS-3081",
            "baselineTitle": "Degraded comms shakeout",
            "summary": "The current run is materially stronger than the degraded comms shakeout, especially in link recovery and queue flush speed.",
            "scoreDelta": 8,
            "largestWindow": "05:14 - 05:17",
            "recommendation": "This profile is safe to promote as the new clean reference for uplink recovery.",
            "focusAreas": [
                {"label": "Link Quality", "current": "94%", "baseline": "86%", "delta": "+8%"},
                {"label": "Reconnect Time", "current": "2.1 s", "baseline": "3.4 s", "delta": "-1.3 s"},
                {"label": "Packet Loss", "current": "0.8%", "baseline": "3.2%", "delta": "-2.4%"},
            ],
        },
    },
}


def _session_index() -> dict[str, dict[str, Any]]:
    return {session["id"]: session for session in SESSIONS}


def list_sessions() -> list[dict[str, Any]]:
    return deepcopy(SESSIONS)


def get_overview() -> dict[str, Any]:
    scores = [session["score"] for session in SESSIONS]
    flagged = sum(1 for session in SESSIONS if session["status"] == "flagged")
    return {
        "sessions": len(SESSIONS),
        "flagged": flagged,
        "avgScore": round(mean(scores)),
        "artifactsReady": sum(len(SESSION_DETAILS[session["id"]]["artifacts"]) for session in SESSIONS),
    }


def get_replay_catalog() -> dict[str, Any]:
    return {
        "overview": get_overview(),
        "sessions": list_sessions(),
        "defaultSessionId": "TRS-3102",
    }


def get_session_detail(session_id: str) -> dict[str, Any]:
    if session_id not in SESSION_DETAILS:
        raise KeyError(session_id)

    session = _session_index()[session_id]
    detail = deepcopy(SESSION_DETAILS[session_id])
    detail["durationSeconds"] = session["durationSeconds"]
    detail["environment"] = session["environment"]
    detail["vehicle"] = session["vehicle"]
    detail["missionProfile"] = session["missionProfile"]
    detail["defaultBaselineId"] = detail["compareCandidates"][0]["id"]
    return detail


def get_session_comparison(session_id: str, baseline_id: str) -> dict[str, Any]:
    try:
        comparison = COMPARISONS[session_id][baseline_id]
    except KeyError as error:
        raise KeyError(f"{session_id}:{baseline_id}") from error

    payload = deepcopy(comparison)
    payload["sessionId"] = session_id
    return payload


def get_debrief_report(session_id: str, baseline_id: str | None = None) -> dict[str, Any]:
    detail = get_session_detail(session_id)
    resolved_baseline_id = baseline_id or detail["defaultBaselineId"]
    comparison = get_session_comparison(session_id, resolved_baseline_id)
    anomaly_count = len(detail["anomalies"])
    highest_severity = detail["anomalies"][0]["severity"] if detail["anomalies"] else "low"

    return {
        "sessionId": detail["id"],
        "sessionTitle": detail["title"],
        "baselineId": comparison["baselineId"],
        "baselineTitle": comparison["baselineTitle"],
        "score": detail["score"],
        "scoreDelta": comparison["scoreDelta"],
        "verdict": detail["verdict"],
        "executiveSummary": (
            f"{detail['title']} ended with a score of {detail['score']} against "
            f"{comparison['baselineTitle']}. The biggest review window was "
            f"{comparison['largestWindow']}, and the recommended next step is: "
            f"{comparison['recommendation']}"
        ),
        "callouts": [
            f"{anomaly_count} anomalies were flagged, with highest severity marked as {highest_severity}.",
            f"Largest comparison window: {comparison['largestWindow']}.",
            comparison["summary"],
        ],
        "recommendedActions": [
            comparison["recommendation"],
            "Attach the comparison export to the handoff package before promotion.",
            "Review the owner-tagged anomaly windows with the next engineer on shift.",
        ],
        "artifactChecklist": [artifact["name"] for artifact in detail["artifacts"]],
    }
