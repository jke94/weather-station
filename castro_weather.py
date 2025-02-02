import argparse
import json
import os
import requests

from datetime import datetime, timedelta

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

def obtener_datos_meteorologicos(station_id:str, api_key:str, date:str) -> dict:
    
    url = f"https://api.weather.com/v2/pws/history/daily?stationId={station_id}&format=json&units=m&date={date}&apiKey={api_key}&numericPrecision=decimal"

    response = requests.get(url)

    if response.status_code != 200:
        return {"error": f"Error getting data: {response.status_code}"}
        
    try:
        data = response.json()

        metric_data = data["observations"][0]['metric']
        
        wind_direction_avg = wind_direction_calculataion(data["observations"][0]["winddirAvg"])
        uvHighRisk = risk_UV_calculation(data["observations"][0]["uvHigh"])

        formatted_date = datetime.strptime(date, "%Y%m%d").strftime("%Y-%m-%d")

        output = {
            "Date": formatted_date,
            "TemperatureHigh": metric_data["tempHigh"],
            "TemperatureAvg": metric_data["tempAvg"],
            "TemperatureLow": metric_data["tempLow"],
            "DewPointHigh": metric_data["dewptHigh"],
            "DewPointLow": metric_data["dewptLow"],
            "DewPointAvg": metric_data["dewptAvg"],
            "HumidityHigh": data["observations"][0]["humidityHigh"],
            "HumidityLow": data["observations"][0]["humidityLow"],
            "HumidityAvg": data["observations"][0]["humidityAvg"],
            "PricipitationTotal": metric_data["precipTotal"],
            "PressureMax": metric_data["pressureMax"],
            "PressureMin": metric_data["pressureMin"],
            "WindSpeedHigh": metric_data["windspeedHigh"],
            "WindSpeedAvg": metric_data["windspeedAvg"],
            "WindGustHigh": metric_data["windgustHigh"],
            "WindGustAvg": metric_data["windgustAvg"],
            "WindDirectionAvg": wind_direction_avg,
            "UvHighRisk": uvHighRisk,
            "UvIndexHigh": data["observations"][0]["uvHigh"],
            "SolarRadiationHigh" : data["observations"][0]["solarRadiationHigh"]
        }

        return output

    except ValueError:
        return {"error": "Error al procesar los datos JSON."}
        

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Obtener datos meteorológicos.")
    parser.add_argument("--station_id", type=str, help="ID de la estación meteorológica.")
    parser.add_argument("--api_key", type=str, help="API Key para acceder a los datos.")

    args = parser.parse_args()

    # Priority: command line arguments > environment variables

    station_id = args.station_id or os.getenv("STATION_ID")
    api_key = args.api_key or os.getenv("API_KEY")
    
    yesterday = datetime.now() - timedelta(days=1)
    yesterday_formatted_date = yesterday.strftime("%Y%m%d")   

    if not station_id or not api_key:
        print("Error: The environment variables STATION_ID and API_KEY must be defined or passed as arguments.")
    else:
        resultado = obtener_datos_meteorologicos(station_id, api_key, yesterday_formatted_date)
        print(json.dumps(resultado, indent=4))