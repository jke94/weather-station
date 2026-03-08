import argparse
import os

from datetime import datetime, timedelta

from services.weather_service import WeatherService
from services.weather_service import fetch_data_real
from services.weather_service import validate_json_real
from services.weather_service import deserialize_weather_data_real

from services.facebook_service import FacebookService, build_post
from services.facebook_create_post_service import create_post

def main(
    weather_underground_station_id:str,
    weather_underground_api_key:str,
    facebook_access_token:str,
    facebook_page_id:str,
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

    print('DATA API -------------------------------------------')
    print(weather_day_summary_report.model_dump_json(indent=4))

    # Call to Facebook service to post weather report.
    facebook_service = FacebookService(create_post, build_post)

    post = facebook_service.post_weather_report(
        facebook_page_id,
        facebook_access_token,
        weather_day_summary_report
    )

    if post == "NONE":
        print("Error in create post process!")
        return -3

    print(f'Created post: {post}')

    return 0

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Obtain weather data.")
    
    # Weather Underground arguments.
    parser.add_argument("--weather_underground_station_id", 
                        type=str, 
                        help="Weather Underground station ID."
    )
    parser.add_argument("--weather_underground_api_key", 
                        type=str, 
                        help="Weather Underground api key."
    )
    
    # Facebook arguments.
    parser.add_argument("--facebook_access_token", type=str, help="Facebook access token")
    parser.add_argument("--facebook_page_id", type=str, help="Facebook page ID")

    args = parser.parse_args()

    # NOTE: Priority: command line arguments > environment variables

    # Weather Underground arguments.
    weather_underground_station_id = args.weather_underground_station_id or os.getenv("WEATHER_UNDERGROUND_STATION_ID")
    weather_underground_api_key = args.weather_underground_api_key or os.getenv("WEATHER_UNDERGROUND_API_KEY")

    # Facebook arguments.
    facebook_access_token = args.facebook_access_token or os.getenv("FACEBOOK_ACCESS_TOKEN")
    facebook_page_id = args.facebook_page_id or os.getenv("FACEBOOK_PAGE_ID")

    yesterday = datetime.now() - timedelta(days=1)
    yesterday_formatted_date = yesterday.strftime("%Y%m%d")

    result = main(
        weather_underground_station_id, 
        weather_underground_api_key, 
        facebook_access_token, 
        facebook_page_id,
        yesterday_formatted_date
    )

    print(f'Main result value: {result}')

