from typing import Callable

from model.report.weather_day_summary_report import WeatherDaySummaryReport

def translate_to_spanish_uv_risk(uv_risk: str) -> str:
    translation = {
        "Low": "Bajo",
        "Medium": "Medio",
        "High": "Alto",
        "Very high": "Muy alto",
        "Extremely high": "Extremo"
    }
    return translation.get(uv_risk, "NONE")

def build_post(weather_day_summary_report: WeatherDaySummaryReport) -> str:

    return (
        f"¡Buenos días Castrocontrigo!\n"
        f"Resumen de ayer 📅 {weather_day_summary_report.Date}:\n\n"
        f"🌡️ Temperatura (ºC):\n"
        f"   Max. {weather_day_summary_report.TemperatureHigh} | "
        f"Min. {weather_day_summary_report.TemperatureLow} | "
        f"Media. {weather_day_summary_report.TemperatureAvg}\n\n"
        f"💧 Humedad (%):\n"
        f"   Max. {weather_day_summary_report.HumidityHigh} | "
        f"Min. {weather_day_summary_report.HumidityLow} | "
        f"Media. {weather_day_summary_report.HumidityAvg}\n\n"
        f"🌧️ Punto de rocío (ºC):\n"
        f"   Max. {weather_day_summary_report.DewPointHigh} | "
        f"Min. {weather_day_summary_report.DewPointLow} | "
        f"Media. {weather_day_summary_report.DewPointAvg}\n\n"
        f"☔ Precipitación: {weather_day_summary_report.PrecipitationTotal} L/m²\n\n"
        f"💨 Viento:\n"
        f"   Medio: {weather_day_summary_report.WindSpeedAvg} km/h | "
        f"Máx. {weather_day_summary_report.WindSpeedHigh} km/h | "
        f"Racha máx.: {weather_day_summary_report.WindGustHigh} km/h\n"
        f"   Racha media: {weather_day_summary_report.WindGustAvg} km/h\n"
        f"   Dirección media: {weather_day_summary_report.WindDirectionAvg}\n\n"
        f"🔽 Presión (mb): Máx. {weather_day_summary_report.PressureMax} | "
        f"Mín. {weather_day_summary_report.PressureMin}\n\n"
        f"☀️ Índice UV máx.: {weather_day_summary_report.UvIndexHigh} "
        f"({translate_to_spanish_uv_risk(weather_day_summary_report.UvHighRisk)})\n\n"
        f"😎 Radiación solar máx.: {weather_day_summary_report.SolarRadiationHigh} W/m²"
    )

class FacebookService:
    def __init__(
        self,
        create_post: Callable[[str, str, str], str],
        build_post: Callable[[WeatherDaySummaryReport], str]
    ):
        self.build_post = build_post
        self.create_post = create_post

    def post_weather_report(
        self, 
        page_id: str,
        access_token: str,
        weather_report: WeatherDaySummaryReport
    ) -> str:
        
        post_content = self.build_post(weather_report)

        return self.create_post(
            page_id,
            access_token,
            post_content
        )
