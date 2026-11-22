import unittest
from types import SimpleNamespace

from weather_station.config import AppConfig


class TestAppConfig(unittest.TestCase):
    def test_command_line_values_override_environment(self):
        args = SimpleNamespace(
            weather_underground_station_id="cli-station",
            weather_underground_api_key=None,
        )
        config = AppConfig.from_args(
            args,
            environ={
                "WEATHER_UNDERGROUND_STATION_ID": "env-station",
                "WEATHER_UNDERGROUND_API_KEY": "env-api-key",
                "REPORT_TIME_ZONE": "Europe/Madrid",
            },
        )

        self.assertEqual(config.station_id, "cli-station")
        self.assertEqual(config.weather_api_key, "env-api-key")

    def test_reads_operational_settings_from_environment(self):
        config = AppConfig.from_sources(environ={
            "REPORT_TIME_ZONE": "UTC",
            "WEATHER_REQUEST_TIMEOUT_SECONDS": "8.5",
            "WEATHER_REQUEST_RETRIES": "0",
            "WEATHER_PUBLISHING_STATE_PATH": "tmp/state.json",
        })

        self.assertEqual(config.report_timezone, "UTC")
        self.assertEqual(config.weather_request_timeout_seconds, 8.5)
        self.assertEqual(config.weather_request_retries, 0)
        self.assertEqual(config.publishing_state_path, "tmp/state.json")

    def test_rejects_invalid_retry_configuration(self):
        with self.assertRaisesRegex(ValueError, "cannot be negative"):
            AppConfig.from_sources(environ={"WEATHER_REQUEST_RETRIES": "-1"})

    def test_rejects_unknown_time_zone(self):
        with self.assertRaisesRegex(ValueError, "Unknown report time zone"):
            AppConfig.from_sources(environ={"REPORT_TIME_ZONE": "Mars/Olympus"})
