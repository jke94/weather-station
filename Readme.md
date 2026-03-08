# weather-station

[![On push master morning_daily_scheduler.py](https://github.com/jke94/weather-station/actions/workflows/master_on_push_morning_daily_scheduler.yml/badge.svg)](https://github.com/jke94/weather-station/actions/workflows/master_on_push_morning_daily_scheduler.yml)

[![Morning daily scheduler yesterday tweet in X (Twitter) at 09h UTC](https://github.com/jke94/weather-station/actions/workflows/morning_daily_scheduler_tweet_in_X.yml/badge.svg)](https://github.com/jke94/weather-station/actions/workflows/morning_daily_scheduler_tweet_in_X.yml)

[![Morning daily scheduler yesterday report 09h UTC](https://github.com/jke94/weather-station/actions/workflows/morning_daily_scheduler.yml/badge.svg)](https://github.com/jke94/weather-station/actions/workflows/morning_daily_scheduler.yml)

## Description

Weather station automatization reports using with Github Actions and X (also knowing as Twitter in the past) daily report publication process. 

The information is obtained from [Weather Underground](https://www.wunderground.com/) platform. Launching HTTP request over the Web API to get information about the weather information sent by our weather station.

Finally it´s reported in X platform:

- X (Twitter) profile: [⛅Tiempo Castrocontrigo](https://x.com/Castro_tiempo)✌️

Here, a picture about the weather station 📸

<p align="center">
  <img src="https://github.com/jke94/weather-station/blob/master/images/profile_photo_weather_station.jpg" 
  alt="Weather station photo" 
  style="max-width:450px; max-height:450px; height:auto;">
</p>

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

3. Get report from previous day and publish post in Facebook platform.

> [!NOTE]
> Meta (Facebook) requires generate a _Long-live-token_ that expires after 60 days: use `generate_facebook_long_lived_token.py` script.

```
python .\src\weather-station\post_morning_daily_post_in_facebook.py `
    --weather_underground_station_id <WEATHER_UNDERGROUND_STATION_ID> `
    --weather_underground_api_key <WEATHER_UNDERGROUND_API_KEY> `
    --facebook_access_token <FACEBOOK_ACCESS_TOKEN> `
    --facebook_page_id <FACEBOOK_PAGE_ID>
```

How to use `generate_facebook_long_lived_token.py` python script:

```
python generate_long_lived_token.py `
  --app_id <FACEBOOK_APP_ID> `
  --app_secret <FACEBOOK_SECRET_APP> `
  --short_token <FACEBOOK_SHORT_TOKEN>
```

- For `app_id` and `app_secret` go to `https://developers.facebook.com/`, go to My Apps, select the app and go to app configuration. On `basic` you can get this data.

- For `short_token` use the `GET /me/accounts` end-point over _Graph API Explorer_ and get `access_token` value.

- Page Id value also can be capture from `GET /me/accounts` response.

## Run unit tests

```
python .\src\weather-station\test\run_unit_tests.py
```

## Useful information used to build this project.

- [Crontab guru](https://crontab.guru/#*/10_*_*_*_*)
- [X Developer portal](https://developer.twitter.com/en/portal/projects-and-apps)