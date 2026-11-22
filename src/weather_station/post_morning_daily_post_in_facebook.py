import argparse
from functools import partial

from weather_station.business_logic.report_date import previous_report_date
from weather_station.config import AppConfig
from weather_station.services.facebook_create_post_service import create_post
from weather_station.services.facebook_service import (
    FacebookService,
    build_post,
)
from weather_station.services.publishing_state import PublicationStateStore
from weather_station.services.weather_service import (
    WeatherService,
    deserialize_weather_data_real,
    fetch_data_real,
    validate_json_real,
)


def main(
    weather_underground_station_id: str | None,
    weather_underground_api_key: str | None,
    facebook_access_token: str | None,
    facebook_page_id: str | None,
    date: str,
    config: AppConfig | None = None,
    retry_unresolved_publication: bool = False,
) -> int:
    config = config or AppConfig.from_sources({
        "WEATHER_UNDERGROUND_STATION_ID": weather_underground_station_id,
        "WEATHER_UNDERGROUND_API_KEY": weather_underground_api_key,
        "FACEBOOK_ACCESS_TOKEN": facebook_access_token,
        "FACEBOOK_PAGE_ID": facebook_page_id,
    })
    if not weather_underground_station_id or not weather_underground_api_key:
        print(
            "WEATHER_UNDERGROUND_STATION_ID and "
            "WEATHER_UNDERGROUND_API_KEY must be configured."
        )
        return -1
    if not facebook_access_token or not facebook_page_id:
        print("FACEBOOK_ACCESS_TOKEN and FACEBOOK_PAGE_ID must be configured.")
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
            "facebook", weather_underground_station_id, date
        )
    state = publication_state.reserve(
        "facebook", weather_underground_station_id, date
    )
    if state == "published":
        print(f"Facebook report for {date} was already published.")
        return 0
    if state != "reserved":
        print(
            f"Facebook publication for {date} is unresolved; "
            "check the Page before clearing its saved state."
        )
        return -4

    print("DATA API -------------------------------------------")
    print(report.model_dump_json(indent=4))
    facebook_service = FacebookService(create_post, build_post)
    post_url = facebook_service.post_weather_report(
        facebook_page_id,
        facebook_access_token,
        report,
    )
    if post_url == "NONE":
        print("Error in create post process!")
        return -3

    publication_state.mark_published(
        "facebook", weather_underground_station_id, date, post_url
    )
    print(f"Created post: {post_url}")
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
    parser.add_argument(
        "--facebook_access_token", help="Facebook access token"
    )
    parser.add_argument("--facebook_page_id", help="Facebook page ID")
    parser.add_argument(
        "--retry-unresolved-publication",
        action="store_true",
        help="Retry only after verifying that no Facebook post was created.",
    )
    args = parser.parse_args()
    config = AppConfig.from_args(args)

    return main(
        config.station_id,
        config.weather_api_key,
        config.facebook_access_token,
        config.facebook_page_id,
        previous_report_date(time_zone=config.report_timezone),
        config,
        args.retry_unresolved_publication,
    )


if __name__ == "__main__":
    raise SystemExit(cli())
