import argparse
import os

from datetime import datetime, timedelta

from services.weather_service import WeatherService
from services.weather_service import fetch_data_real
from services.weather_service import validate_json_real
from services.weather_service import deserialize_weather_data_real

def main(station_id:str, api_key:str, date:str) -> int:
    
    if not station_id or not api_key:

        print({"error" : "The environment variables STATION_ID and API_KEY must be defined as environment variables or passed as arguments."})
        return -1
    
    # Call to the weather service to get the data inyecting functions.
    weather_service = WeatherService(
        fetch_data=fetch_data_real,
        validate_json=validate_json_real,
        deserialize_weather_data=deserialize_weather_data_real
    )

    weather_day_summary_report = weather_service.build_weather_day_summary_report(
        station_id, api_key, date
    )

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