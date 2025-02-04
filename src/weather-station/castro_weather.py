import argparse
import json
import jsonschema
import os
import requests

from datetime import datetime, timedelta
from jsonschema import validate
from typing import Optional

from business_logic.calculate_risk_uv import calculate_risk_uv
from business_logic.calculate_wind_direction import calculate_wind_direction

from model.pws.history.daily.weather_response import WeatherResponse
from model.report.weather_day_summary_report import WeatherDaySummaryReport

def load_json_schema(schema_path: str):
    with open(schema_path, "r", encoding="utf-8") as file:
        return json.load(file)

def build_weather_day_summary_report(station_id:str, api_key:str, date:str) -> Optional[WeatherDaySummaryReport]:
    
    try:

        url = f"https://api.weather.com/v2/pws/history/daily?stationId={station_id}&format=json&units=m&date={date}&apiKey={api_key}&numericPrecision=decimal"

        response = requests.get(url)

        if response.status_code != 200:

            print({"error" : f"Error getting data. HTTP code: {response.status_code}."})

            return None

        # Get data.
        data = response.json()

        # Load JSON schema to validate the response.
        schema = load_json_schema("./json-schema/v2/pws-history-daily.json")
        
        # Validate data against the schema.
        validate(instance=data, schema=schema)

        # Deserialize data against the previously defined model.
        weather_response = WeatherResponse(**data)
        
        # Bussines logic to convert data.
        wind_direction_avg = calculate_wind_direction(weather_response.observations[0].winddirAvg)
        uv_high_risk = calculate_risk_uv(weather_response.observations[0].uvHigh)
        formatted_date = datetime.strptime(date, "%Y%m%d").strftime("%Y-%m-%d")

        # Generate output model.
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

        return {"error" : f"HTTP request failed: {e}"}

    except ValueError:

        return {"error" : "Error al procesar los datos JSON."}
    
    except jsonschema.exceptions.ValidationError as e:

        return {"error" : f"JSON Schema validation failed: {e}"}    

def main(station_id:str, api_key:str, date:str) -> int:
    
    if not station_id or not api_key:

        print({"error" : "The environment variables STATION_ID and API_KEY must be defined as environment variables or passed as arguments."})
        return -1
    
    weather_day_summary_report = build_weather_day_summary_report(station_id, api_key, date)

    if weather_day_summary_report == None:
        
        print({"error" : "Error trying to get data."})
        return -2
    
    print(weather_day_summary_report.model_dump_json(indent=4))

    return 0

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Obtain weather data.")
    parser.add_argument("--station_id", type=str, help="Weather station ID.")
    parser.add_argument("--api_key", type=str, help="API Key para acceder a los datos.")

    args = parser.parse_args()

    # Priority: command line arguments > environment variables

    station_id = args.station_id or os.getenv("STATION_ID")
    api_key = args.api_key or os.getenv("API_KEY")
    
    yesterday = datetime.now() - timedelta(days=1)
    yesterday_formatted_date = yesterday.strftime("%Y%m%d")

    result = main(station_id, api_key, yesterday_formatted_date)