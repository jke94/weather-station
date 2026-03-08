import unittest
from unittest.mock import MagicMock
from model.report.weather_day_summary_report import WeatherDaySummaryReport
from services.facebook_service import FacebookService, build_post, translate_to_spanish_uv_risk

class TestFacebookService(unittest.TestCase):

    def setUp(self):
        """Configure mocks"""
        self.mock_create_post = MagicMock(return_value="https://www.facebook.com/123456789")

        self.weather_report = WeatherDaySummaryReport(
            Date="2024-03-15",
            TemperatureHigh=22.8,
            TemperatureAvg=15.3,
            TemperatureLow=8.9,
            DewPointHigh=12.5,
            DewPointLow=4.2,
            DewPointAvg=8.6,
            HumidityHigh=85.0,
            HumidityLow=35.0,
            HumidityAvg=58.3,
            PrecipitationTotal=3.2,
            PressureMax=1015.77,
            PressureMin=1010.45,
            WindSpeedHigh=15.2,
            WindSpeedAvg=8.3,
            WindGustHigh=22.1,
            WindGustAvg=10.7,
            WindDirectionAvg="SSW",
            UvHighRisk="High",
            UvIndexHigh=7.5,
            SolarRadiationHigh=680.4
        )

        self.facebook_service = FacebookService(
            create_post=self.mock_create_post,
            build_post=build_post
        )

    def test_build_post_generates_correct_message(self):

        # Arrange
        expected_values = [
            f"¡Buenos días Castrocontrigo!",
            f"Resumen de ayer 📅 {self.weather_report.Date}",
            f"🌡️ Temperatura (ºC):",
            f"Max. {self.weather_report.TemperatureHigh} | "
            f"Min. {self.weather_report.TemperatureLow} | "
            f"Media. {self.weather_report.TemperatureAvg}",
            f"💧 Humedad (%):",
            f"Max. {self.weather_report.HumidityHigh} | "
            f"Min. {self.weather_report.HumidityLow} | "
            f"Media. {self.weather_report.HumidityAvg}",
            f"🌧️ Punto de rocío (ºC):",
            f"Max. {self.weather_report.DewPointHigh} | "
            f"Min. {self.weather_report.DewPointLow} | "
            f"Media. {self.weather_report.DewPointAvg}",
            f"☔ Precipitación: {self.weather_report.PrecipitationTotal} L/m²",
            f"💨 Viento:",
            f"Medio: {self.weather_report.WindSpeedAvg} km/h | "
            f"Máx. {self.weather_report.WindSpeedHigh} km/h | "
            f"Racha máx.: {self.weather_report.WindGustHigh} km/h",
            f"Racha media: {self.weather_report.WindGustAvg} km/h",
            f"Dirección media: {self.weather_report.WindDirectionAvg}",
            f"🔽 Presión (mb): Máx. {self.weather_report.PressureMax} | "
            f"Mín. {self.weather_report.PressureMin}",
            f"☀️ Índice UV máx.: {self.weather_report.UvIndexHigh} "
            f"({translate_to_spanish_uv_risk(self.weather_report.UvHighRisk)})",
            f"😎 Radiación solar máx.: {self.weather_report.SolarRadiationHigh} W/m²"
        ]

        # Act
        post = build_post(self.weather_report)

        # Assert
        for value in expected_values:
            with self.subTest(value=value):
                self.assertIn(value, post)

    def test_post_weather_report_calls_create_post_correctly(self):
        """Act: Call `post_weather_report`. Assert: Validate call to `create_post`."""

        post_url = self.facebook_service.post_weather_report(
            "PAGE_ID_FAKE", 
            "ACCESS_TOKEN_FAKE", 
            self.weather_report
        )

        self.mock_create_post.assert_called_once_with(
            "PAGE_ID_FAKE", 
            "ACCESS_TOKEN_FAKE", 
            build_post(self.weather_report)
        )

        self.assertEqual(post_url, "https://www.facebook.com/123456789")

    def test_translate_to_spanish_uv_risk(self):
        """Act & Assert: Testing translation of different UV levels."""

        self.assertEqual(translate_to_spanish_uv_risk("Low"), "Bajo")
        self.assertEqual(translate_to_spanish_uv_risk("Medium"), "Medio")
        self.assertEqual(translate_to_spanish_uv_risk("High"), "Alto")
        self.assertEqual(translate_to_spanish_uv_risk("Very high"), "Muy alto")
        self.assertEqual(translate_to_spanish_uv_risk("Extremely high"), "Extremo")
        self.assertEqual(translate_to_spanish_uv_risk("Unknown"), "NONE")
