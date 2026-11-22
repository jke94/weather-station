# weather-station

[![On push master morning_daily_scheduler_on_x.py](https://github.com/jke94/weather-station/actions/workflows/master_on_push_morning_daily_scheduler.yml/badge.svg)](https://github.com/jke94/weather-station/actions/workflows/master_on_push_morning_daily_scheduler.yml)

[![Morning daily scheduler yesterday tweet in X (Twitter) at 09h UTC](https://github.com/jke94/weather-station/actions/workflows/morning_daily_scheduler_tweet_in_X.yml/badge.svg)](https://github.com/jke94/weather-station/actions/workflows/morning_daily_scheduler_tweet_in_X.yml)

[![Morning daily scheduler yesterday post in Facebook at 09h UTC](https://github.com/jke94/weather-station/actions/workflows/morning_daily_scheduler_tweet_in_facebook.yml/badge.svg?branch=master)](https://github.com/jke94/weather-station/actions/workflows/morning_daily_scheduler_tweet_in_facebook.yml)

## Description

Weather station automatization reports using with Github Actions and X (also knowing as Twitter in the past) daily report publication process. 

The information is obtained from [Weather Underground](https://www.wunderground.com/) platform. Launching HTTP request over the Web API to get information about the weather information sent by our weather station.

Finally, reports are published on these platforms:

| Platform | Profile | Link |
| --- | --- | --- |
| X (Twitter) | ⛅Tiempo Castrocontrigo | [Visit profile](https://x.com/Castro_tiempo) |
| Facebook | ⛅Tiempo Castrocontrigo | [Visit page](https://www.facebook.com/profile.php?id=61588289686123) |

The Facebook daily post includes temperature, wind chill (sensible temperature),
heat index, humidity, dew point, precipitation, wind, pressure, UV index, and
solar radiation from the PWS daily history.

Here, a picture about the weather station 📸

<p align="center">
  <img src="./images/profile_photo_weather_station.jpg"
    alt="Weather station photo"
    width="450">
</p>

## How to run

The scripts read configuration from command-line arguments, environment
variables, or a local `.env` file (in that precedence order). Keep secrets out
of source control.

The package lives in `src/weather_station`. Create a virtual environment,
install the **requirements.txt** packages, and set `PYTHONPATH` before running
the module CLIs.

### Linux and macOS

Run these commands from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export PYTHONPATH=src
```

Print a report about the weather station:

```bash
python -m weather_station.morning_daily_scheduler_on_x \
    --weather_underground_station_id <WEATHER_UNDERGROUND_STATION_ID> \
    --weather_underground_api_key <WEATHER_UNDERGROUND_API_KEY>
```

Publish the previous day's report on X:

```bash
python -m weather_station.post_morning_daily_tweet_in_x \
    --weather_underground_station_id <WEATHER_UNDERGROUND_STATION_ID> \
    --weather_underground_api_key <WEATHER_UNDERGROUND_API_KEY> \
    --x_api_key <X_API_KEY> \
    --x_api_key_secret <X_API_KEY_SECRET> \
    --x_access_token <X_ACCESS_TOKEN> \
    --x_access_secret_token <X_ACCESS_SECRET_TOKEN>
```

Publish the previous day's report on Facebook:

```bash
python -m weather_station.post_morning_daily_post_in_facebook \
    --weather_underground_station_id <WEATHER_UNDERGROUND_STATION_ID> \
    --weather_underground_api_key <WEATHER_UNDERGROUND_API_KEY> \
    --facebook_access_token <FACEBOOK_ACCESS_TOKEN> \
    --facebook_page_id <FACEBOOK_PAGE_ID>
```

Generate a long-lived Facebook token:

```bash
python src/utils/generate_facebook_long_lived_token.py \
    --app_id <FACEBOOK_APP_ID> \
    --app_secret <FACEBOOK_SECRET_APP> \
    --short_token <FACEBOOK_SHORT_TOKEN>
```

### Windows (PowerShell)

Run these commands from the repository root:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r .\requirements.txt
$env:PYTHONPATH = "src"
```

Print a report about the weather station:

```powershell
python -m weather_station.morning_daily_scheduler_on_x `
    --weather_underground_station_id <WEATHER_UNDERGROUND_STATION_ID> `
    --weather_underground_api_key <WEATHER_UNDERGROUND_API_KEY>
```

Publish the previous day's report on X:

```powershell
python -m weather_station.post_morning_daily_tweet_in_x `
    --weather_underground_station_id <WEATHER_UNDERGROUND_STATION_ID> `
    --weather_underground_api_key <WEATHER_UNDERGROUND_API_KEY> `
    --x_api_key <X_API_KEY> `
    --x_api_key_secret <X_API_KEY_SECRET> `
    --x_access_token <X_ACCESS_TOKEN> `
    --x_access_secret_token <X_ACCESS_SECRET_TOKEN>
```

Publish the previous day's report on Facebook:

```powershell
python -m weather_station.post_morning_daily_post_in_facebook `
    --weather_underground_station_id <WEATHER_UNDERGROUND_STATION_ID> `
    --weather_underground_api_key <WEATHER_UNDERGROUND_API_KEY> `
    --facebook_access_token <FACEBOOK_ACCESS_TOKEN> `
    --facebook_page_id <FACEBOOK_PAGE_ID>
```

Generate a long-lived Facebook token:

```powershell
python .\src\utils\generate_facebook_long_lived_token.py `
    --app_id <FACEBOOK_APP_ID> `
    --app_secret <FACEBOOK_SECRET_APP> `
    --short_token <FACEBOOK_SHORT_TOKEN>
```

> [!NOTE]
> Use `generate_facebook_long_lived_token.py` to exchange a short-lived user
> token for a long-lived user token. Token lifetime depends on Meta's policies
> and the token's permissions; check the returned expiration rather than
> assuming a fixed duration.
> If publishing fails, the workflow logs the Graph API response details alongside
> the HTTP status. Check the returned error message and code before changing the
> token or Page configuration; never share access tokens in logs or reports.

- For `app_id` and `app_secret`, open `https://developers.facebook.com/`, select **My Apps**, choose the app, and open **App settings → Basic**. The App ID and App Secret must be from the same app.

- Generate `short_token` in **Graph API Explorer** with this same app selected. It must be a short-lived **user** access token with the permissions needed to access the Page. Do not use the Page token returned by `/me/accounts` as the short token for this exchange.

- After the exchange, use `GET /me/accounts?fields=id,name,access_token` with the long-lived user token to retrieve the Page ID and Page access token. Use the Page access token for publishing.
- Keep the App Secret and all access tokens private. Do not commit them, paste them into issues, or include them in logs. The script accepts the values as command-line arguments or from `FACEBOOK_APP_ID`, `FACEBOOK_APP_SECRET`, and `FACEBOOK_SHORT_TOKEN` environment variables.

## Optional configuration

The following variables have defaults and can be overridden in the environment
or `.env` file:

| Variable | Default | Description |
| --- | --- | --- |
| `REPORT_TIME_ZONE` | `Europe/Madrid` | Time zone used to determine the previous report day |
| `WEATHER_REQUEST_TIMEOUT_SECONDS` | `15` | Timeout for a weather API request |
| `WEATHER_REQUEST_RETRIES` | `3` | Maximum retries for transient weather-read errors |
| `WEATHER_PUBLISHING_STATE_PATH` | `.weather_station/publishing-state.json` | Local publication-state file |

Weather reads retry transient connection, timeout, rate-limit, and server errors
with a bounded backoff. Post creation is not automatically retried. The
publishing workflows persist their idempotency state as a GitHub Actions
artifact for 90 days and serialize runs per platform. If a run reports an
unresolved publication, check the platform before manually dispatching the
workflow with `retry_unresolved_publication` enabled.

## Run unit tests

Activate the virtual environment as shown above, then run the test command.

### Linux and macOS

```bash
python -m test.run_unit_tests
```

### Windows (PowerShell)

```powershell
python -m test.run_unit_tests
```

## Useful information used to build this project.

- [Crontab guru](https://crontab.guru/#*/10_*_*_*_*)
- [X developer portal](https://developer.twitter.com/en/portal/projects-and-apps)
- [Facebook developers portal](https://developers.facebook.com)