import tweepy
from typing import Callable, Optional

from model.report.weather_day_summary_report import WeatherDaySummaryReport

def trasnlate_to_spanish_uv_risk(uv_risk:str) -> str:

    value = "_"

    match uv_risk:
        case "Low":
            value = "Bajo"
        case "Medium":
            value = "Medio"
        case "High":
            value = "Alto"
        case "Very high":
            value = "Muy alto"                        
        case "Extremely high":
            value = "Extremo"                        
        case "Very high":
            value = "Muy alto"                        
        case _:
            value = "NONE"

    return value

def build_tweet(weather_day_summary_report: WeatherDaySummaryReport) -> str:
    
    date_str = weather_day_summary_report.Date

    temperature_max = weather_day_summary_report.TemperatureHigh
    temperature_low = weather_day_summary_report.TemperatureLow
    temperature_avg = weather_day_summary_report.TemperatureAvg
    precipitation_total = weather_day_summary_report.PrecipitationTotal    
    wind_speed_avg = weather_day_summary_report.WindSpeedAvg
    wind_direction_avg = weather_day_summary_report.WindDirectionAvg
    wind_gust_high = weather_day_summary_report.WindGustHigh    
    uv_high = weather_day_summary_report.UvIndexHigh
    uv_risk = weather_day_summary_report.UvHighRisk
    solar_radiation_high = weather_day_summary_report.SolarRadiationHigh
    
    msg = (
        f"¡Buenos días Castrocontrigo!\n"
        f"Resumen de ayer 📅 {date_str}:\n\n"
        f"🌡️ Temp. (ºC): Max. {temperature_max} | Min. {temperature_low} | Media. {temperature_avg}\n"
        f"💧 Lluvia: {precipitation_total} L/m²\n"             
        f"💨 Viento medio: {wind_speed_avg} km/h | Dir. media: {wind_direction_avg}\n"
        f"🌀 Racha viento max.: {wind_gust_high} km/h\n"
        f"☀️ Índice UV max.: {uv_high} ({trasnlate_to_spanish_uv_risk(uv_risk)})\n"
        f"😎 Radiación solar max.: {solar_radiation_high} W/m²"
    )

    return msg

def create_tweet(
    api_key_for_x:str,
    api_key_secret_for_x:str,
    access_token_for_x:str,
    access_secret_token_for_x:str,
    tweet_content:str    
) -> str:

    created_tweet_url = "NONE"

    try:
        
        # Create X (Twitter) client.
        client = tweepy.Client(
            consumer_key=api_key_for_x, 
            consumer_secret=api_key_secret_for_x,
            access_token=access_token_for_x, 
            access_token_secret=access_secret_token_for_x
        )

        response = client.create_tweet(
            text=tweet_content
        )

        created_tweet_url = f"https://twitter.com/user/status/{response.data['id']}"

        return created_tweet_url

    except Exception as error:
        
        print({'error': f"Create tweet HTTP status code: {error}"})
        return created_tweet_url

class TwitterService:

    def __init__(
        self,
        create_tweet: Callable[[str, str, str, str, str], str],
        build_tweet: Callable[[WeatherDaySummaryReport], str]
        ):      
        self.build_tweet = build_tweet
        self.create_tweet = create_tweet