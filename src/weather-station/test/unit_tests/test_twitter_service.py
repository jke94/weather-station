import unittest
from unittest.mock import MagicMock
from model.report.weather_day_summary_report import WeatherDaySummaryReport
from services.twitter_service import TwitterService, build_tweet, translate_to_spanish_uv_risk

class TestTwitterService(unittest.TestCase):

    def setUp(self):
        """Configure mocks"""
        self.mock_create_tweet = MagicMock(return_value="https://twitter.com/user/status/123456789")

        self.weather_report = WeatherDaySummaryReport(
            Date="2024-02-03",
            TemperatureHigh=14.4,
            TemperatureAvg=7.7,
            TemperatureLow=2.2,
            DewPointHigh=6.4,
            DewPointLow=-0.8,
            DewPointAvg=2.7,
            HumidityHigh=99.0,
            HumidityLow=40.0,
            HumidityAvg=72.7,
            PrecipitationTotal=15.6,
            PressureMax=1008.13,
            PressureMin=1002.37,
            WindSpeedHigh=19.8,
            WindSpeedAvg=4.6,
            WindGustHigh=25.4,
            WindGustAvg=6.3,
            WindDirectionAvg="WNW",
            UvHighRisk="Medium",
            UvIndexHigh=5.0,
            SolarRadiationHigh=460.1
        )

        self.twitter_service = TwitterService(
            create_tweet=self.mock_create_tweet,
            build_tweet=build_tweet
        )

    def test_build_tweet_generates_correct_message(self):

        # Arrange
        expected_values = [
            f"Resumen de ayer 📅 {self.weather_report.Date}",
            f"🌡️ Temp. (ºC): Max. {self.weather_report.TemperatureHigh} | "
            f"Min. {self.weather_report.TemperatureLow} | "
            f"Media. {self.weather_report.TemperatureAvg}",
            f"💧 Lluvia: {self.weather_report.PrecipitationTotal} L/m²",
            f"💨 Viento medio: {self.weather_report.WindSpeedAvg} km/h | "
            f"Dir. media: {self.weather_report.WindDirectionAvg}",
            f"🌀 Racha viento max.: {self.weather_report.WindGustHigh} km/h",
            f"☀️ Índice UV max.: {self.weather_report.UvIndexHigh} "
            f"({translate_to_spanish_uv_risk(self.weather_report.UvHighRisk)})",
            f"😎 Radiación solar max.: {self.weather_report.SolarRadiationHigh} W/m²"
        ]

        # Act
        tweet = build_tweet(self.weather_report)

        # Assert
        for value in expected_values:
            with self.subTest(value=value):
                self.assertIn(value, tweet)

    def test_post_weather_report_calls_create_tweet_correctly(self):
        """Act: Call `post_weather_report`. Assert: Validate call to `create_tweet`."""

        tweet_url = self.twitter_service.post_weather_report(
            "API_KEY_FAKE", 
            "API_SECRET_FAKE", 
            "ACCESS_TOKEN_FAKE", 
            "ACCESS_SECRET_FAKE", self.weather_report
        )

        self.mock_create_tweet.assert_called_once_with(
            "API_KEY_FAKE", 
            "API_SECRET_FAKE", 
            "ACCESS_TOKEN_FAKE", 
            "ACCESS_SECRET_FAKE", 
            build_tweet(self.weather_report)
        )

        self.assertEqual(tweet_url, "https://twitter.com/user/status/123456789")

    def test_translate_to_spanish_uv_risk(self):
        """Act & Assert: Testing translation of different UV levels."""

        self.assertEqual(translate_to_spanish_uv_risk("Low"), "Bajo")
        self.assertEqual(translate_to_spanish_uv_risk("Medium"), "Medio")
        self.assertEqual(translate_to_spanish_uv_risk("High"), "Alto")
        self.assertEqual(translate_to_spanish_uv_risk("Very high"), "Muy alto")
        self.assertEqual(translate_to_spanish_uv_risk("Extremely high"), "Extremo")
        self.assertEqual(translate_to_spanish_uv_risk("Unknown"), "NONE")