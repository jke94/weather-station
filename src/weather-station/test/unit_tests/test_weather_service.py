import unittest
from unittest.mock import MagicMock
from services.weather_service import WeatherService
from model.report.weather_day_summary_report import WeatherDaySummaryReport
from model.pws.history.daily.weather_response import WeatherResponse

class TestWeatherService(unittest.TestCase):
    def setUp(self):
        self.mock_fetch_data = MagicMock(return_value={
            "observations": [
                {
                    "stationID": "ICASTR328",
                    "tz": "Europe/Madrid",
                    "obsTimeUtc": "2025-02-01T22:58:58Z",
                    "obsTimeLocal": "2025-02-01 23:58:58",
                    "epoch": 1738450738,
                    "lat": 42.187863,
                    "lon": -6.191118,
                    "solarRadiationHigh": 460.1,
                    "uvHigh": 5.0,
                    "winddirAvg": 303,
                    "humidityHigh": 99.0,
                    "humidityLow": 40.0,
                    "humidityAvg": 72.7,
                    "qcStatus": -1,
                    "metric": {
                        "tempHigh": 14.4,
                        "tempLow": 2.2,
                        "tempAvg": 7.7,
                        "windspeedHigh": 19.8,
                        "windspeedLow": 0.0,
                        "windspeedAvg": 4.6,
                        "windgustHigh": 25.4,
                        "windgustLow": 0.0,
                        "windgustAvg": 6.3,
                        "dewptHigh": 6.4,
                        "dewptLow": -0.8,
                        "dewptAvg": 2.7,
                        "windchillHigh": 14.4,
                        "windchillLow": 1.0,
                        "windchillAvg": 7.5,
                        "heatindexHigh": 14.4,
                        "heatindexLow": 2.2,
                        "heatindexAvg": 7.7,
                        "pressureMax": 1008.13,
                        "pressureMin": 1002.37,
                        "pressureTrend": -0.24,
                        "precipRate": 0.00,
                        "precipTotal": 15.6
                    }
                }
            ]
        })
        
        self.mock_validate_json = MagicMock(return_value=True)
        weather_response_obj = WeatherResponse(**self.mock_fetch_data.return_value)

        self.mock_deserialize_weather_data = MagicMock(return_value=weather_response_obj)

        self.weather_service = WeatherService(
            fetch_data=self.mock_fetch_data,
            validate_json=self.mock_validate_json,
            deserialize_weather_data=self.mock_deserialize_weather_data
        )

    def test_build_weather_day_summary_report(self):
        
        # Arrange
        station_id = "TEST123"
        api_key = "FAKE_API_KEY"
        date = "20240203"

        # Act
        report = self.weather_service.build_weather_day_summary_report(
            station_id, 
            api_key, 
            date
        )

        # Assert
        self.assertIsInstance(report, WeatherDaySummaryReport)

        self.assertEqual(report.Date, "2024-02-03")
        self.assertEqual(report.TemperatureHigh, 14.4)
        self.assertEqual(report.TemperatureAvg, 7.7)
        self.assertEqual(report.TemperatureLow, 2.2)
        self.assertEqual(report.DewPointHigh, 6.4)
        self.assertEqual(report.DewPointLow, -0.8)
        self.assertEqual(report.DewPointAvg, 2.7)
        self.assertEqual(report.HumidityHigh, 99.0)
        self.assertEqual(report.HumidityLow, 40.0)
        self.assertEqual(report.HumidityAvg, 72.7)
        self.assertEqual(report.PrecipitationTotal, 15.6)
        self.assertEqual(report.PressureMax, 1008.13)
        self.assertEqual(report.PressureMin, 1002.37)
        self.assertEqual(report.WindSpeedHigh, 19.8)
        self.assertEqual(report.WindSpeedAvg, 4.6)
        self.assertEqual(report.WindGustHigh, 25.4)
        self.assertEqual(report.WindGustAvg, 6.3)
        self.assertEqual(report.WindDirectionAvg, "WNW")
        self.assertEqual(report.UvHighRisk, "Medium")
        self.assertEqual(report.UvIndexHigh, 5.0)
        self.assertEqual(report.SolarRadiationHigh, 460.1)
