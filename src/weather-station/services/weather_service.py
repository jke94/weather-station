import requests
import jsonschema
import json

from datetime import datetime
from typing import Callable, Optional
from dataclasses import dataclass

from model.pws.history.daily.weather_response import WeatherResponse
from model.report.weather_day_summary_report import WeatherDaySummaryReport

from business_logic.calculate_risk_uv import calculate_risk_uv
from business_logic.calculate_wind_direction import calculate_wind_direction

class WeatherService:
    def __init__(
        self, 
        fetch_data: Callable[[str], dict], 
        validate_json: Callable[[dict], bool],
        deserialize_weather_data: Callable[[dict], WeatherResponse]
    ):
        """Allows you to inject functions to get data, validate JSON, and deserialize"""
        self.fetch_data = fetch_data
        self.validate_json = validate_json
        self.deserialize_weather_data = deserialize_weather_data

    def build_weather_day_summary_report(self, station_id: str, api_key: str, date: str) -> Optional[WeatherDaySummaryReport]:

        try:
            url = f"https://api.weather.com/v2/pws/history/daily?stationId={station_id}&format=json&units=m&date={date}&apiKey={api_key}&numericPrecision=decimal"

            # Inyection to get the data.
            data = self.fetch_data(url)  
            
            # Inyection to validate JSON.
            if not self.validate_json(data):  
                print({"error": "JSON Schema validation failed."})
                return None

            # Inyection to deserialize_weather_data
            weather_response = self.deserialize_weather_data(data)  

            # Lógica de conversión
            wind_direction_avg = calculate_wind_direction(weather_response.observations[0].winddirAvg)
            uv_high_risk = calculate_risk_uv(weather_response.observations[0].uvHigh)
            formatted_date = datetime.strptime(date, "%Y%m%d").strftime("%Y-%m-%d")

            return WeatherDaySummaryReport(
                Date=formatted_date,
                TemperatureHigh=weather_response.observations[0].metric.tempHigh,
                TemperatureAvg=weather_response.observations[0].metric.tempAvg,
                TemperatureLow=weather_response.observations[0].metric.tempLow,
                DewPointHigh=weather_response.observations[0].metric.dewptHigh,
                DewPointLow=weather_response.observations[0].metric.dewptLow,
                DewPointAvg=weather_response.observations[0].metric.dewptAvg,
                HumidityHigh=weather_response.observations[0].humidityHigh,
                HumidityLow=weather_response.observations[0].humidityLow,
                HumidityAvg=weather_response.observations[0].humidityAvg,
                PrecipitationTotal=weather_response.observations[0].metric.precipTotal,
                PressureMax=weather_response.observations[0].metric.pressureMax,
                PressureMin=weather_response.observations[0].metric.pressureMin,
                WindSpeedHigh=weather_response.observations[0].metric.windspeedHigh,
                WindSpeedAvg=weather_response.observations[0].metric.windgustAvg,
                WindGustHigh=weather_response.observations[0].metric.windgustHigh,
                WindGustAvg=weather_response.observations[0].metric.windgustAvg,
                WindDirectionAvg=wind_direction_avg,
                UvHighRisk=uv_high_risk,
                UvIndexHigh=weather_response.observations[0].uvHigh,
                SolarRadiationHigh=weather_response.observations[0].solarRadiationHigh
            )

        except requests.exceptions.RequestException as e:
            return {"error": f"HTTP request failed: {e}"}

        except ValueError:
            return {"error": "Error al procesar los datos JSON."}

        except jsonschema.exceptions.ValidationError as e:
            return {"error": f"JSON Schema validation failed: {e}"}
        
def fetch_data_real(url: str) -> dict:

    response = requests.get(url)
    response.raise_for_status()
    
    return response.json()

def load_json_schema(schema_path: str):

    with open(schema_path, "r", encoding="utf-8") as file:
        return json.load(file)

def validate_json_real(data: dict) -> bool:

    schema = load_json_schema("./json-schema/v2/pws-history-daily.json")
    
    try:
        jsonschema.validate(instance=data, schema=schema)
        return True
    except jsonschema.exceptions.ValidationError:
        return False

def deserialize_weather_data_real(data: dict) -> WeatherResponse:
    return WeatherResponse(**data)        