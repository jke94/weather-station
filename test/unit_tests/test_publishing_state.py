import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile
from unittest.mock import Mock, patch

from weather_station.services.publishing_state import PublicationStateStore

SOURCE_DIRECTORY = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "src")
)
sys.path.insert(0, SOURCE_DIRECTORY)

from utils.restore_publishing_state import restore_latest_state


class TestPublicationStateStore(unittest.TestCase):
    def test_published_reports_are_not_reserved_again(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            state = PublicationStateStore(str(path))

            self.assertEqual(
                state.reserve("x", "station", "20261121"), "reserved"
            )
            self.assertEqual(
                state.reserve("x", "station", "20261121"), "publishing"
            )
            self.assertTrue(
                state.clear_unresolved("x", "station", "20261121")
            )
            self.assertEqual(
                state.reserve("x", "station", "20261121"), "reserved"
            )

            state.mark_published(
                "x", "station", "20261121", "https://x.example/post"
            )
            self.assertFalse(
                state.clear_unresolved("x", "station", "20261121")
            )
            self.assertEqual(
                state.reserve("x", "station", "20261121"), "published"
            )

            saved_state = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(
                saved_state["x:station:20261121"]["url"],
                "https://x.example/post",
            )

    def test_station_and_date_have_independent_state(self):
        with tempfile.TemporaryDirectory() as directory:
            state = PublicationStateStore(
                str(Path(directory) / "state.json")
            )

            self.assertEqual(
                state.reserve("facebook", "station-a", "20261121"),
                "reserved",
            )
            self.assertEqual(
                state.reserve("facebook", "station-b", "20261121"),
                "reserved",
            )
            self.assertEqual(
                state.reserve("facebook", "station-a", "20261120"),
                "reserved",
            )


class TestRestorePublishingState(unittest.TestCase):
    @patch("utils.restore_publishing_state._github_api_get")
    def test_restores_latest_matching_artifact(self, mock_api_get):
        workflow_response = Mock()
        workflow_response.json.return_value = {
            "workflow_runs": [{
                "id": 42,
                "created_at": "2026-11-21T09:00:00Z",
            }]
        }
        artifact_response = Mock()
        artifact_response.json.return_value = {
            "artifacts": [{
                "name": "weather-station-state-x",
                "expired": False,
                "archive_download_url": "https://api.example/archive",
            }]
        }
        archive_buffer = io.BytesIO()
        with zipfile.ZipFile(archive_buffer, "w") as archive:
            archive.writestr(
                "publishing-state.json",
                '{"x:station:20261121":'
                '{"status":"published","url":"https://x.example/post"}}',
            )
        archive_response = Mock(content=archive_buffer.getvalue())
        mock_api_get.side_effect = [
            workflow_response,
            artifact_response,
            archive_response,
        ]

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state" / "publishing-state.json"
            restore_latest_state(
                platform="x",
                state_path=path,
                token="token",
                repository="owner/repo",
                workflow_ref="owner/repo/.github/workflows/x.yml@refs/heads/main",
                branch="main",
                current_run_id="100",
                api_url="https://api.example",
            )

            state = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(
            state["x:station:20261121"]["status"], "published"
        )
        self.assertEqual(mock_api_get.call_count, 3)

    @patch("utils.restore_publishing_state._github_api_get")
    def test_creates_empty_state_when_no_artifact_exists(self, mock_api_get):
        workflow_response = Mock()
        workflow_response.json.return_value = {"workflow_runs": []}
        mock_api_get.return_value = workflow_response

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            restore_latest_state(
                platform="facebook",
                state_path=path,
                token="token",
                repository="owner/repo",
                workflow_ref=(
                    "owner/repo/.github/workflows/facebook.yml@refs/heads/main"
                ),
                branch="main",
                current_run_id="100",
                api_url="https://api.example",
            )

            self.assertEqual(json.loads(path.read_text(encoding="utf-8")), {})
