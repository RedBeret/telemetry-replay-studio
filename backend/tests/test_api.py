from __future__ import annotations

import sys
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.main import app


class TelemetryReplayStudioApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)

    def test_healthcheck(self) -> None:
        response = self.client.get("/api/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_replay_catalog(self) -> None:
        response = self.client.get("/api/replay")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["defaultSessionId"], "TRS-3102")
        self.assertGreaterEqual(len(payload["sessions"]), 3)
        self.assertIn("overview", payload)

    def test_session_detail(self) -> None:
        response = self.client.get("/api/replay/TRS-3102")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["id"], "TRS-3102")
        self.assertEqual(payload["defaultBaselineId"], "TRS-3098")
        self.assertGreaterEqual(len(payload["signalFrames"]), 4)
        self.assertGreaterEqual(len(payload["anomalies"]), 1)

    def test_comparison_endpoint(self) -> None:
        response = self.client.get("/api/replay/TRS-3102/compare/TRS-3098")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["baselineId"], "TRS-3098")
        self.assertEqual(payload["sessionId"], "TRS-3102")
        self.assertGreaterEqual(len(payload["focusAreas"]), 3)

    def test_debrief_endpoint(self) -> None:
        response = self.client.get("/api/replay/TRS-3102/debrief?baseline_id=TRS-3098")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["sessionId"], "TRS-3102")
        self.assertIn("executiveSummary", payload)
        self.assertGreaterEqual(len(payload["recommendedActions"]), 2)

    def test_missing_session_returns_404(self) -> None:
        response = self.client.get("/api/replay/TRS-9999")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Session not found")

    def test_missing_comparison_returns_404(self) -> None:
        response = self.client.get("/api/replay/TRS-3102/compare/TRS-9999")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Comparison not found")


if __name__ == "__main__":
    unittest.main()
