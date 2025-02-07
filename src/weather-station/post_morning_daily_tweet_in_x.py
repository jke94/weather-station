import argparse
import os
import tweepy

from datetime import datetime, timedelta

from services.weather_service import WeatherService
from services.weather_service import fetch_data_real
from services.weather_service import validate_json_real
from services.weather_service import deserialize_weather_data_real

from model.report.weather_day_summary_report import WeatherDaySummaryReport

def build_tweet(weather_day_summary_report: WeatherDaySummaryReport) -> str:
    
    date_str = weather_day_summary_report.Date  # TODO: Format
    wind_gust_high = weather_day_summary_report.WindGustHigh
    wind_speed_avg = weather_day_summary_report.WindSpeedAvg
    temperature_max = weather_day_summary_report.TemperatureHigh
    temperature_low = weather_day_summary_report.TemperatureLow
    precipitation_total = weather_day_summary_report.PrecipitationTotal
    uv_high = weather_day_summary_report.UvIndexHigh
    uv_risk = weather_day_summary_report.UvHighRisk
    
    msg = (
        f"¡Buenos días Castrocontrigo!\n"
        f"Resumen de ayer 📅 {date_str}:\n\n"
        f"💨 Viento : {wind_speed_avg} km/h [W]\n"
        f"🌀 Racha: {wind_gust_high} km/h\n"
        f"🌡️ Temperatura: Max {temperature_max} °C | Min {temperature_low} C\n"
        f"💧 Lluvia: {precipitation_total} L/m²\n"
        f"☀️ Índice UV: {uv_high} [{uv_risk}]"
    )

    return msg

def main(
    weather_underground_station_id:str,
    weather_underground_api_key:str,
    api_key_for_x:str,
    api_key_secret_for_x:str,
    access_token_for_x:str,
    access_secret_token_for_x:str,
    date:str
) -> int:

    # Input functions parameter validation
    if not weather_underground_station_id or not weather_underground_api_key:

        error = {
                "error" : """The environment variables 
                    WEATHER_UNDERGROUND_STATION_ID and WEATHER_UNDERGROUND_API_KEY 
                    must be defined as environment variables or passed as arguments."""
                }

        print(error)
            
        return -1



    # Call to the weather service to get the data inyecting functions.
    weather_service = WeatherService(
        fetch_data=fetch_data_real,
        validate_json=validate_json_real,
        deserialize_weather_data=deserialize_weather_data_real
    )

    # Get report
    weather_day_summary_report = weather_service.build_weather_day_summary_report(
        weather_underground_station_id, 
        weather_underground_api_key, 
        date
    )

    if weather_day_summary_report == None:
        
        print({"error" : "Error trying to get data."})
        return -2

    print(weather_day_summary_report.model_dump_json(indent=4))

    # Build message
    text_message = build_tweet(weather_day_summary_report)
    print('--------------------------------------')
    print(text_message)
    print('--------------------------------------')
    print(f'Tweet length: {len(text_message)}')


    # TODO: Uncomment for tweet publication

    # Create X (Twitter) client.
    # client = tweepy.Client(
    #     consumer_key=api_key_for_x, 
    #     consumer_secret=api_key_secret_for_x,
    #     access_token=access_token_for_x, 
    #     access_token_secret=access_secret_token_for_x
    # )

    # response = client.create_tweet(
    #     text=text_message
    # )

    # print(f"https://twitter.com/user/status/{response.data['id']}")

    # response.close()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Obtain weather data.")
    
    # Weather Underground
    parser.add_argument("--weather_underground_station_id", 
                        type=str, 
                        help="Weather Underground station ID.", 
                        required=True
    )
    parser.add_argument("--weather_underground_api_key", 
                        type=str, 
                        help="Weather Underground api Key.", 
                        required=True
    )
    
    # X (Twitter) arguments.
    parser.add_argument("--x_api_key", type=str, help="X (Twitter) api key", required=True)
    parser.add_argument("--x_api_key_secret", type=str, help="X (Twitter) secret api key", required=True)
    parser.add_argument("--x_access_token", type=str, help="X (Twitter) access token", required=True)
    parser.add_argument("--x_access_secret_token", type=str, help="X (Twitter) access secret token", required=True)

    args = parser.parse_args()

    # NOTE: Priority: command line arguments > environment variables

    # Weather Underground arguments.
    weather_underground_station_id = args.weather_underground_station_id or os.getenv("WEATHER_UNDERGROUND_STATION_ID")
    weather_underground_api_key = args.weather_underground_api_key or os.getenv("WEATHER_UNDERGROUND_API_KEY")

    # X (Twitter) arguments.
    x_api_key = args.x_api_key or os.getenv("X_API_KEY")
    x_api_key_secret = args.x_api_key_secret or os.getenv("X_API_KEY_SECRET")
    x_access_token = args.x_access_token or os.getenv("X_ACCESS_TOKEN")
    x_access_secret_token = args.x_access_secret_token or os.getenv("X_ACCESS_SECRET_TOKEN")

    yesterday = datetime.now() - timedelta(days=1)
    yesterday_formatted_date = yesterday.strftime("%Y%m%d")

    result = main(
        weather_underground_station_id, 
        weather_underground_api_key, 
        x_api_key, 
        x_api_key_secret, 
        x_access_token, 
        x_access_secret_token,
        yesterday_formatted_date
    )

    print(f'Main result value: {result}')