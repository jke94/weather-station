import json
import time
from datetime import datetime
from pathlib import Path
from typing import Callable
from urllib.parse import quote, quote_plus

import jsonschema
import requests

from weather_station.business_logic.calculate_risk_uv import calculate_risk_uv
from weather_station.business_logic.calculate_wind_direction import (
    calculate_wind_direction,
)
from weather_station.config import AppConfig
from weather_station.model.pws.history.daily.weather_response import (
    WeatherResponse,
)
from weather_station.model.report.weather_day_summary_report import (
    WeatherDaySummaryReport,
)

RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}


def _redact_api_key(message: str, api_key: str) -> str:
    if not api_key:
        return message

    for secret in {
        api_key,
        quote(api_key, safe=""),
        quote_plus(api_key),
    }:
        message = message.replace(secret, "[REDACTED]")
    return message


class WeatherService:
    def __init__(
        self,
        fetch_data: Callable[[str], dict],
        validate_json: Callable[[dict], bool],
        deserialize_weather_data: Callable[[dict], WeatherResponse],
    ):
        """Inject data fetching, validation, and deserialization functions."""
        self.fetch_data = fetch_data
        self.validate_json = validate_json
        self.deserialize_weather_data = deserialize_weather_data

    def build_weather_day_summary_report(
        self, station_id: str, api_key: str, date: str
    ) -> WeatherDaySummaryReport | None:
        try:
            url = (
                "https://api.weather.com/v2/pws/history/daily?"
                f"stationId={station_id}&format=json&units=m&date={date}"
                f"&apiKey={api_key}&numericPrecision=decimal"
            )

            data = self.fetch_data(url)
            if not self.validate_json(data):
                print({"error": "JSON Schema validation failed."})
                return None

            weather_response = self.deserialize_weather_data(data)
            observation = weather_response.observations[0]
            wind_direction_avg = calculate_wind_direction(
                observation.winddirAvg
            )
            uv_high_risk = calculate_risk_uv(observation.uvHigh)
            formatted_date = datetime.strptime(date, "%Y%m%d").strftime("%Y-%m-%d")

            return WeatherDaySummaryReport(
                Date=formatted_date,
                TemperatureHigh=observation.metric.tempHigh,
                TemperatureAvg=observation.metric.tempAvg,
                TemperatureLow=observation.metric.tempLow,
                DewPointHigh=observation.metric.dewptHigh,
                DewPointLow=observation.metric.dewptLow,
                DewPointAvg=observation.metric.dewptAvg,
                WindChillHigh=observation.metric.windchillHigh,
                WindChillLow=observation.metric.windchillLow,
                WindChillAvg=observation.metric.windchillAvg,
                HeatIndexHigh=observation.metric.heatindexHigh,
                HeatIndexLow=observation.metric.heatindexLow,
                HeatIndexAvg=observation.metric.heatindexAvg,
                HumidityHigh=observation.humidityHigh,
                HumidityLow=observation.humidityLow,
                HumidityAvg=observation.humidityAvg,
                PrecipitationTotal=observation.metric.precipTotal,
                PressureMax=observation.metric.pressureMax,
                PressureMin=observation.metric.pressureMin,
                WindSpeedHigh=observation.metric.windspeedHigh,
                WindSpeedAvg=observation.metric.windspeedAvg,
                WindGustHigh=observation.metric.windgustHigh,
                WindGustAvg=observation.metric.windgustAvg,
                WindDirectionAvg=wind_direction_avg,
                UvHighRisk=uv_high_risk,
                UvIndexHigh=observation.uvHigh,
                SolarRadiationHigh=observation.solarRadiationHigh,
            )

        except requests.exceptions.RequestException as e:
            print({
                "error": (
                    "HTTP request failed: "
                    f"{_redact_api_key(str(e), api_key)}"
                )
            })
            return None

        except ValueError as e:
            print({"error": f"Error al procesar los datos JSON: {e}"})
            return None

        except jsonschema.exceptions.ValidationError as e:
            print({"error": f"JSON Schema validation failed: {e}"})
            return None


def fetch_data_real(
    url: str, config: AppConfig | None = None
) -> dict:
    config = config or AppConfig.from_sources()
    for attempt in range(config.weather_request_retries + 1):
        try:
            response = requests.get(
                url, timeout=config.weather_request_timeout_seconds
            )
            response.raise_for_status()
            return response.json()
        except (
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
        ):
            if attempt == config.weather_request_retries:
                raise
        except requests.exceptions.HTTPError as error:
            status_code = error.response.status_code if error.response else None
            if (
                status_code not in RETRYABLE_STATUS_CODES
                or attempt == config.weather_request_retries
            ):
                raise

        time.sleep(2**attempt)

    raise RuntimeError("Weather request retry loop exited unexpectedly.")

def load_json_schema(schema_path: str):
    path = Path(schema_path)
    if not path.is_absolute():
        path = Path(__file__).resolve().parents[3] / path
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)

def validate_json_real(data: dict) -> bool:
    schema = load_json_schema("json-schema/v2/pws-history-daily.json")

    try:
        jsonschema.validate(instance=data, schema=schema)
        return True
    except jsonschema.exceptions.ValidationError:
        return False

def deserialize_weather_data_real(data: dict) -> WeatherResponse:
    return WeatherResponse(**data)