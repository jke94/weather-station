from typing import Callable

from weather_station.model.report.weather_day_summary_report import (
    WeatherDaySummaryReport,
)

def translate_to_spanish_uv_risk(uv_risk: str) -> str:
    translation = {
        "Low": "Bajo",
        "Medium": "Medio",
        "High": "Alto",
        "Very high": "Muy alto",
        "Extremely high": "Extremo"
    }
    return translation.get(uv_risk, "NONE")

def build_tweet(weather_day_summary_report: WeatherDaySummaryReport) -> str:

    return (
        f"¡Buenos días Castrocontrigo!\n"
        f"Resumen de ayer 📅 {weather_day_summary_report.Date}:\n\n"
        f"🌡️ Temp. (ºC): Max. {weather_day_summary_report.TemperatureHigh} | "
        f"Min. {weather_day_summary_report.TemperatureLow} | "
        f"Media. {weather_day_summary_report.TemperatureAvg}\n"
        f"💧 Lluvia: {weather_day_summary_report.PrecipitationTotal} L/m²\n"
        f"💨 Viento medio: {weather_day_summary_report.WindSpeedAvg} km/h | "
        f"Dir. media: {weather_day_summary_report.WindDirectionAvg}\n"
        f"🌀 Racha viento max.: {weather_day_summary_report.WindGustHigh} km/h\n"
        f"☀️ Índice UV max.: {weather_day_summary_report.UvIndexHigh} "
        f"({translate_to_spanish_uv_risk(weather_day_summary_report.UvHighRisk)})\n"
        f"😎 Radiación solar max.: {weather_day_summary_report.SolarRadiationHigh} W/m²"
    )

class TwitterService:
    def __init__(
        self,
        create_tweet: Callable[[str, str, str, str, str], str],
        build_tweet: Callable[[WeatherDaySummaryReport], str]
    ):
        self.build_tweet = build_tweet
        self.create_tweet = create_tweet

    def post_weather_report(
        self, 
        api_key: str, 
        api_secret: str, 
        access_token: str, 
        access_secret: str, 
        weather_report: WeatherDaySummaryReport
    ) -> str:
        
        tweet_content = self.build_tweet(weather_report)

        return self.create_tweet(
            api_key,
            api_secret, 
            access_token, 
            access_secret, 
            tweet_content
        )