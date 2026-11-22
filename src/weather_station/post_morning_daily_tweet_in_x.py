import argparse
from functools import partial

from weather_station.business_logic.report_date import previous_report_date
from weather_station.config import AppConfig
from weather_station.services.publishing_state import PublicationStateStore
from weather_station.services.twitter_create_post_service import create_tweet
from weather_station.services.twitter_service import (
    TwitterService,
    build_tweet,
)
from weather_station.services.weather_service import (
    WeatherService,
    deserialize_weather_data_real,
    fetch_data_real,
    validate_json_real,
)


def main(
    weather_underground_station_id: str | None,
    weather_underground_api_key: str | None,
    api_key_for_x: str | None,
    api_key_secret_for_x: str | None,
    access_token_for_x: str | None,
    access_secret_token_for_x: str | None,
    date: str,
    config: AppConfig | None = None,
    retry_unresolved_publication: bool = False,
) -> int:
    config = config or AppConfig.from_sources({
        "WEATHER_UNDERGROUND_STATION_ID": weather_underground_station_id,
        "WEATHER_UNDERGROUND_API_KEY": weather_underground_api_key,
        "X_API_KEY": api_key_for_x,
        "X_API_KEY_SECRET": api_key_secret_for_x,
        "X_ACCESS_TOKEN": access_token_for_x,
        "X_ACCESS_SECRET_TOKEN": access_secret_token_for_x,
    })
    if not weather_underground_station_id or not weather_underground_api_key:
        print(
            "WEATHER_UNDERGROUND_STATION_ID and "
            "WEATHER_UNDERGROUND_API_KEY must be configured."
        )
        return -1
    if (
        not api_key_for_x
        or not api_key_secret_for_x
        or not access_token_for_x
        or not access_secret_token_for_x
    ):
        print(
            "X_API_KEY, X_API_KEY_SECRET, X_ACCESS_TOKEN, and "
            "X_ACCESS_SECRET_TOKEN must be configured."
        )
        return -1

    weather_service = WeatherService(
        fetch_data=partial(fetch_data_real, config=config),
        validate_json=validate_json_real,
        deserialize_weather_data=deserialize_weather_data_real,
    )
    report = weather_service.build_weather_day_summary_report(
        weather_underground_station_id,
        weather_underground_api_key,
        date,
    )
    if report is None:
        print({"error": "Error trying to get data."})
        return -2

    publication_state = PublicationStateStore(
        path=config.publishing_state_path
    )
    if retry_unresolved_publication:
        publication_state.clear_unresolved(
            "x", weather_underground_station_id, date
        )
    state = publication_state.reserve(
        "x", weather_underground_station_id, date
    )
    if state == "published":
        print(f"X report for {date} was already published.")
        return 0
    if state != "reserved":
        print(
            f"X publication for {date} is unresolved; "
            "check the profile before clearing its saved state."
        )
        return -4

    print("DATA API -------------------------------------------")
    print(report.model_dump_json(indent=4))
    twitter_service = TwitterService(create_tweet, build_tweet)
    tweet_url = twitter_service.post_weather_report(
        api_key_for_x,
        api_key_secret_for_x,
        access_token_for_x,
        access_secret_token_for_x,
        report,
    )
    if tweet_url == "NONE":
        print("Error in create tweet process!")
        return -3

    publication_state.mark_published(
        "x", weather_underground_station_id, date, tweet_url
    )
    print(f"Created tweet: {tweet_url}")
    return 0


def cli() -> int:
    parser = argparse.ArgumentParser(description="Obtain weather data.")
    parser.add_argument(
        "--weather_underground_station_id",
        help="Weather Underground station ID.",
    )
    parser.add_argument(
        "--weather_underground_api_key",
        help="Weather Underground API key.",
    )
    parser.add_argument("--x_api_key", help="X (Twitter) API key")
    parser.add_argument(
        "--x_api_key_secret", help="X (Twitter) secret API key"
    )
    parser.add_argument("--x_access_token", help="X (Twitter) access token")
    parser.add_argument(
        "--x_access_secret_token", help="X (Twitter) access secret token"
    )
    parser.add_argument(
        "--retry-unresolved-publication",
        action="store_true",
        help="Retry only after verifying that no X post was created.",
    )
    args = parser.parse_args()
    config = AppConfig.from_args(args)

    return main(
        config.station_id,
        config.weather_api_key,
        config.x_api_key,
        config.x_api_key_secret,
        config.x_access_token,
        config.x_access_secret_token,
        previous_report_date(time_zone=config.report_timezone),
        config,
        args.retry_unresolved_publication,
    )


if __name__ == "__main__":
    raise SystemExit(cli())
