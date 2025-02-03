import argparse
import json
import jsonschema
import os
import requests

from jsonschema import validate
from datetime import datetime, timedelta

from model.pws.history.daily.weather_response import WeatherResponse

def wind_direction_calculataion(wind_direction_avg:int) -> str:

    wind_directions = [
        "N", 
        "NNE", 
        "NE", 
        "ENE",
        "E", 
        "ESE", 
        "SE", 
        "SSE",
        "S", 
        "SSW", 
        "SW", 
        "WSW", 
        "W", 
        "WNW", 
        "NW", 
        "NNW"
    ]
    
    wind_direction = wind_directions[int((wind_direction_avg % 360) / 22.5)]

    return wind_direction

def risk_UV_calculation(uv:int) -> str:

    if 0 <= uv <= 2:
        return "Low"
    elif 3 <= uv <= 5:
        return "Medium"
    elif 6 <= uv <= 7:
        return "High"
    elif 8 <= uv <= 10:
        return "Very high"
    elif 11 <= uv:
        return "Extremely high"

    return "NONE"

def load_json_schema(schema_path: str):
    with open(schema_path, "r", encoding="utf-8") as file:
        return json.load(file)

def get_weather_data(station_id:str, api_key:str, date:str) -> dict:
    
    try:

        url = f"https://api.weather.com/v2/pws/history/daily?stationId={station_id}&format=json&units=m&date={date}&apiKey={api_key}&numericPrecision=decimal"

        response = requests.get(url)

        schema = load_json_schema("./json-schema/v2/pws-history-daily.json")

        if response.status_code != 200:

            return {"error": f"❌ Error getting data: {response.status_code}"}

        # Get data.
        data = response.json()
        
        # Validate data against the schema
        validate(instance=data, schema=schema)

        # Deserialize data against the previously defined model
        weather_response = WeatherResponse(**data)
        
        # Bussines logic to convert data.
        wind_direction_avg = wind_direction_calculataion(weather_response.observations[0].winddirAvg)
        uv_high_risk = risk_UV_calculation(weather_response.observations[0].uvHigh)
        formatted_date = datetime.strptime(date, "%Y%m%d").strftime("%Y-%m-%d")

        # Generate output model.
        output = {
            "Date": formatted_date,
            "TemperatureHigh": weather_response.observations[0].metric.tempHigh,
            "TemperatureAvg": weather_response.observations[0].metric.tempAvg,
            "TemperatureLow": weather_response.observations[0].metric.tempLow,
            "DewPointHigh": weather_response.observations[0].metric.dewptHigh,
            "DewPointLow": weather_response.observations[0].metric.dewptLow,
            "DewPointAvg": weather_response.observations[0].metric.dewptAvg,
            "HumidityHigh": weather_response.observations[0].humidityHigh,
            "HumidityLow": weather_response.observations[0].humidityLow,
            "HumidityAvg":  weather_response.observations[0].humidityAvg,
            "PricipitationTotal": weather_response.observations[0].metric.precipTotal,
            "PressureMax": weather_response.observations[0].metric.pressureMax,
            "PressureMin": weather_response.observations[0].metric.pressureMin,
            "WindSpeedHigh": weather_response.observations[0].metric.windspeedHigh,
            "WindSpeedAvg": weather_response.observations[0].metric.windgustAvg,
            "WindGustHigh": weather_response.observations[0].metric.windgustHigh,
            "WindGustAvg": weather_response.observations[0].metric.windgustAvg,
            "WindDirectionAvg": wind_direction_avg,
            "UvHighRisk": uv_high_risk,
            "UvIndexHigh": weather_response.observations[0].uvHigh,
            "SolarRadiationHigh" : weather_response.observations[0].solarRadiationHigh
        }

        return output

    except requests.exceptions.RequestException as e:

        return {"error": f"❌ HTTP request failed: {e}"}

    except ValueError:

        return {"error": "❌ Error al procesar los datos JSON."}
    
    except jsonschema.exceptions.ValidationError as e:

        return {"error": f"❌ JSON Schema validation failed: {e}"}    

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

    result = {}

    if not station_id or not api_key:
        result = {"error":"❌ The environment variables STATION_ID and API_KEY must be defined or passed as arguments."}
    else:
        result = get_weather_data(station_id, api_key, yesterday_formatted_date)

    print(json.dumps(result, indent=4))