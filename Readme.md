# weather-station

Weather station automatization reports using with Github Actions and X (also knowing as Twitter in the past) daily report publication process. 

The information is obtained from [Weather Underground](https://www.wunderground.com/) platform. Launching HTTP request over the Web API to get information about the weather information sent by our weather station.

Finally it´s reported in X platform [
⛅Tiempo Castrocontrigo](https://x.com/Castro_tiempo)✌️

<p align="center">
  <figure>
    <img src="https://github.com/jke94/weather-station/blob/master/images/profile_photo_weather_station.jpg" 
    alt="Weather station photo" 
    style="max-width:450px; max-height:450px; height:auto;">
    <figcaption style="text-align:center; font-size:14px; color:gray;">Weather Station photo</figcaption>
  </figure>
</p>

Github actio status:

- [![On push master morning_daily_scheduler.py](https://github.com/jke94/weather-station/actions/workflows/master_on_push_castro_weather.yml/badge.svg)](https://github.com/jke94/weather-station/actions/workflows/master_on_push_castro_weather.yml)

- [![Morning daily scheduler yesterday tweet in X (Twitter) at 09h UTC](https://github.com/jke94/weather-station/actions/workflows/morning_daily_scheduler_tweet_in_X.yml/badge.svg)](https://github.com/jke94/weather-station/actions/workflows/morning_daily_scheduler_tweet_in_X.yml)

- [![Morning daily scheduler yesterday report 09h UTC](https://github.com/jke94/weather-station/actions/workflows/morning_daily_scheduler.yml/badge.svg)](https://github.com/jke94/weather-station/actions/workflows/morning_daily_scheduler.yml)



## How to run

0. Recommended create python virtual environment and install **requirements.txt** packages.

```
python -m venv venv
```

```
.\venv\Scripts\activate
```

```
pip install -r .\requirements.txt
```
Note: **scripts using by default environment variables** but, you can use also input arguments.

1. Get report about weather station and print in console.

```
python .\src\weather-station\test\morning_daily_scheduler.py `
    --weather_underground_station_id <WEATHER_UNDERGROUND_STATION_ID> `
    --weather_underground_api_key <WEATHER_UNDERGROUND_API_KEY> 
```

2. Get report from previous day and publish tweet in X (Twitter) platform.

```
python .\src\weather-station\post_morning_daily_tweet_in_x.py `
    --weather_underground_station_id <WEATHER_UNDERGROUND_STATION_ID> `
    --weather_underground_api_key <WEATHER_UNDERGROUND_API_KEY> `
    --x_api_key <X_API_KEY> `
    --x_api_key_secret <X_API_KEY_SECRET> `
    --x_access_token <X_ACCESS_TOKEN> `
    --x_access_secret_token <X_ACCESS_SECRET_TOKEN>
```

## Run unit tests

```
python .\src\weather-station\test\run_unit_tests.py
```

## Useful information used to build this project.

- [Crontab guru](https://crontab.guru/#*/10_*_*_*_*)
- [X Developer portal](https://developer.twitter.com/en/portal/projects-and-apps)