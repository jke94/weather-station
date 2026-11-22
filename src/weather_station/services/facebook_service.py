from datetime import datetime
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


def _format_number(value: float) -> str:
    return f"{value:g}".replace(".", ",")


def build_post(weather_day_summary_report: WeatherDaySummaryReport) -> str:
    report = weather_day_summary_report
    formatted_date = datetime.strptime(report.Date, "%Y-%m-%d").strftime(
        "%d/%m/%Y"
    )

    return (
        f"⛅ Castrocontrigo · Resumen de ayer ({formatted_date})\n\n"
        f"🌡️ Temperatura: "
        f"{_format_number(report.TemperatureHigh)} °C máx. · "
        f"{_format_number(report.TemperatureAvg)} °C media · "
        f"{_format_number(report.TemperatureLow)} °C mín.\n"
        f"🥶 Sensación térmica: "
        f"{_format_number(report.WindChillHigh)} °C máx. · "
        f"{_format_number(report.WindChillAvg)} °C media · "
        f"{_format_number(report.WindChillLow)} °C mín.\n"
        f"🔥 Índice de calor: "
        f"{_format_number(report.HeatIndexHigh)} °C máx. · "
        f"{_format_number(report.HeatIndexAvg)} °C media · "
        f"{_format_number(report.HeatIndexLow)} °C mín.\n\n"
        f"💧 Humedad: "
        f"{_format_number(report.HumidityHigh)} % máx. · "
        f"{_format_number(report.HumidityAvg)} % media · "
        f"{_format_number(report.HumidityLow)} % mín.\n"
        f"🌧️ Precipitación: "
        f"{_format_number(report.PrecipitationTotal)} mm\n"
        f"💨 Viento: "
        f"{_format_number(report.WindSpeedHigh)} km/h máx. · "
        f"{_format_number(report.WindSpeedAvg)} km/h media\n"
        f"   Racha máx.: {_format_number(report.WindGustHigh)} km/h · "
        f"Dirección media: {report.WindDirectionAvg}\n"
        f"🌫️ Punto de rocío: "
        f"{_format_number(report.DewPointHigh)} °C máx. · "
        f"{_format_number(report.DewPointAvg)} °C media · "
        f"{_format_number(report.DewPointLow)} °C mín.\n\n"
        f"🔽 Presión: "
        f"{_format_number(report.PressureMax)} hPa máx. · "
        f"{_format_number(report.PressureMin)} hPa mín.\n"
        f"☀️ UV máx.: {_format_number(report.UvIndexHigh)} "
        f"({translate_to_spanish_uv_risk(report.UvHighRisk)}) · "
        f"Radiación solar máx.: "
        f"{_format_number(report.SolarRadiationHigh)} W/m²"
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
