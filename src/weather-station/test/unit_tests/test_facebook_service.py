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
            WindChillHigh=22.8,
            WindChillLow=8.9,
            WindChillAvg=15.3,
            HeatIndexHigh=22.8,
            HeatIndexLow=8.9,
            HeatIndexAvg=15.3,
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
        post = build_post(self.weather_report)

        expected_post = (
            "⛅ Castrocontrigo · Resumen de ayer (15/03/2024)\n\n"
            "🌡️ Temperatura: 22,8 °C máx. · 15,3 °C media · 8,9 °C mín.\n"
            "🥶 Sensación térmica: 22,8 °C máx. · 15,3 °C media · "
            "8,9 °C mín.\n"
            "🔥 Índice de calor: 22,8 °C máx. · 15,3 °C media · "
            "8,9 °C mín.\n\n"
            "💧 Humedad: 85 % máx. · 58,3 % media · 35 % mín.\n"
            "🌧️ Precipitación: 3,2 mm\n"
            "💨 Viento: 15,2 km/h máx. · 8,3 km/h media\n"
            "   Racha máx.: 22,1 km/h · Dirección media: SSW\n"
            "🌫️ Punto de rocío: 12,5 °C máx. · 8,6 °C media · "
            "4,2 °C mín.\n\n"
            "🔽 Presión: 1015,77 hPa máx. · 1010,45 hPa mín.\n"
            "☀️ UV máx.: 7,5 (Alto) · "
            "Radiación solar máx.: 680,4 W/m²"
        )

        self.assertEqual(post, expected_post)

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
