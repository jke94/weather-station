import argparse
import json
import requests
import os

def wind_direction_calcultaion(wind_direction_avg:int) -> str:

    if 0 <= wind_direction_avg <= 22.5 or 337.5 <= wind_direction_avg <= 360:
        return "N"
    elif 22.5 <= wind_direction_avg < 67.5:
        return "NE"
    elif 67.5 <= wind_direction_avg < 112.5:
        return "E" 
    elif 112.5 <= wind_direction_avg < 157.5:
        return "SE"
    elif 157.5 <= wind_direction_avg < 202.5:
        return "S"
    elif 202.5 <= wind_direction_avg < 247.5:
        return "SW"
    elif 247.5 <= wind_direction_avg < 292.5:
        return "W"
    elif 292.5 <= wind_direction_avg < 337.5:
        return "NW"    
    
    return "NONE"

def index_UV_calculation(uv:int) -> str:

    if 0 <= uv <= 2:
        return "Bajo"
    elif 3 <= uv <= 5:
        return "Moderado"
    elif 6 <= uv <= 7:
        return "Alto"
    elif 8 <= uv <= 10:
        return "Muy alto"
    elif 11 <= uv <= 100:
        return "Extremo"

    return "NONE"

def obtener_datos_meteorologicos(station_id:str, api_key:str) -> dict:
    
    url = f"https://api.weather.com/v2/pws/dailysummary/3day?apiKey={api_key}&stationId={station_id}&numericPrecision=decimal&format=json&units=m"

    response = requests.get(url)

    if response.status_code != 200:
        return {"error": f"Error getting data: {response.status_code}"}
        
    try:
        data = response.json()

        # Get data.
        tempHigh = data['summaries'][1]['metric']['tempHigh']
        tempLow = data['summaries'][1]['metric']['tempLow']
        precipTotal = data['summaries'][1]['metric']['precipTotal']
        pressureMax = data['summaries'][1]['metric']['pressureMax']
        pressureMin = data['summaries'][1]['metric']['pressureMin']
        windspeedAvg = data['summaries'][1]['metric']['windspeedAvg']
        windgustHigh = data['summaries'][1]['metric']['windgustHigh']
        uvHigh = data['summaries'][0]['uvHigh']
        winddirAvg = data['summaries'][0]['winddirAvg']
        
        wind_direction = wind_direction_calcultaion(winddirAvg)
        uv_high = index_UV_calculation(uvHigh)

        # Data output
        output = {
            "tempHigh": tempHigh,
            "tempLow": tempLow,
            "precipTotal": precipTotal,
            "pressureMax": pressureMax,
            "pressureMin": pressureMin,
            "windspeedAvg": windspeedAvg,
            "windgustHigh": windgustHigh,
            "winddirAvg": winddirAvg,
            "uvHigh": uvHigh,
            "WindDirec": wind_direction,
            "uvHighLetter": uv_high
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

    if not station_id or not api_key:
        print("Error: The environment variables STATION_ID and API_KEY must be defined or passed as arguments.")
    else:
        resultado = obtener_datos_meteorologicos(station_id, api_key)
        print(json.dumps(resultado, indent=4))