from datetime import datetime, timezone
import unittest
from unittest.mock import Mock, patch

import requests

from weather_station.business_logic.report_date import previous_report_date
from weather_station.config import AppConfig
from weather_station.services.weather_service import (
    fetch_data_real,
)


class TestPreviousReportDate(unittest.TestCase):
    def test_uses_madrid_date_when_utc_is_previous_day(self):
        now = datetime(2026, 1, 1, 23, 30, tzinfo=timezone.utc)

        self.assertEqual(previous_report_date(now), "20260101")

    def test_handles_spring_dst_transition(self):
        now = datetime(2026, 3, 29, 22, 30, tzinfo=timezone.utc)

        self.assertEqual(previous_report_date(now), "20260329")

    def test_handles_autumn_dst_transition(self):
        now = datetime(2026, 10, 25, 23, 30, tzinfo=timezone.utc)

        self.assertEqual(previous_report_date(now), "20261025")

    def test_rejects_naive_datetime(self):
        with self.assertRaisesRegex(ValueError, "timezone-aware"):
            previous_report_date(datetime(2026, 1, 1))


class TestWeatherRequestRetries(unittest.TestCase):
    @patch("weather_station.services.weather_service.time.sleep")
    @patch("weather_station.services.weather_service.requests.get")
    def test_retries_timeout_then_returns_response(self, mock_get, mock_sleep):
        response = Mock()
        response.json.return_value = {"observations": []}
        config = AppConfig.from_sources(environ={
            "WEATHER_REQUEST_RETRIES": "2",
        })
        mock_get.side_effect = [
            requests.exceptions.Timeout("slow response"),
            response,
        ]

        self.assertEqual(
            fetch_data_real("https://weather.example", config),
            {"observations": []},
        )
        self.assertEqual(mock_get.call_count, 2)
        self.assertEqual(mock_get.call_args.kwargs["timeout"], 15.0)
        mock_sleep.assert_called_once_with(1)

    @patch("weather_station.services.weather_service.time.sleep")
    @patch("weather_station.services.weather_service.requests.get")
    def test_retries_server_error(self, mock_get, mock_sleep):
        failed_response = Mock(status_code=503)
        failed_response.raise_for_status.side_effect = (
            requests.exceptions.HTTPError(response=failed_response)
        )
        successful_response = Mock()
        successful_response.json.return_value = {"observations": []}
        mock_get.side_effect = [failed_response, successful_response]
        config = AppConfig.from_sources(environ={
            "WEATHER_REQUEST_RETRIES": "1",
        })

        self.assertEqual(
            fetch_data_real("https://weather.example", config),
            {"observations": []},
        )

        self.assertEqual(mock_get.call_count, 2)
        mock_sleep.assert_called_once_with(1)

    @patch("weather_station.services.weather_service.time.sleep")
    @patch("weather_station.services.weather_service.requests.get")
    def test_does_not_retry_bad_request(self, mock_get, mock_sleep):
        response = Mock()
        response.status_code = 400
        error = requests.exceptions.HTTPError(response=response)
        response.raise_for_status.side_effect = error
        mock_get.return_value = response

        with self.assertRaises(requests.exceptions.HTTPError):
            fetch_data_real("https://weather.example")

        mock_get.assert_called_once()
        mock_sleep.assert_not_called()

    @patch("weather_station.services.weather_service.time.sleep")
    @patch("weather_station.services.weather_service.requests.get")
    def test_stops_after_retry_limit(self, mock_get, mock_sleep):
        mock_get.side_effect = requests.exceptions.Timeout("offline")
        config = AppConfig.from_sources(environ={
            "WEATHER_REQUEST_RETRIES": "2",
        })

        with self.assertRaises(requests.exceptions.Timeout):
            fetch_data_real("https://weather.example", config)

        self.assertEqual(mock_get.call_count, 3)
        self.assertEqual(mock_sleep.call_count, 2)
