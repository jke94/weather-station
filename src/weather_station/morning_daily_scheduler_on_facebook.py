import argparse
from functools import partial

from weather_station.business_logic.report_date import previous_report_date
from weather_station.config import AppConfig
from weather_station.services.facebook_service import build_post
from weather_station.services.weather_service import (
    WeatherService,
    deserialize_weather_data_real,
    fetch_data_real,
    validate_json_real,
)


def main(
    station_id: str | None,
    api_key: str | None,
    date: str,
    config: AppConfig | None = None,
) -> int:
    config = config or AppConfig.from_sources({
        "WEATHER_UNDERGROUND_STATION_ID": station_id,
        "WEATHER_UNDERGROUND_API_KEY": api_key,
    })
    if not station_id or not api_key:
        print(
            "WEATHER_UNDERGROUND_STATION_ID and "
            "WEATHER_UNDERGROUND_API_KEY must be configured."
        )
        return -1

    weather_service = WeatherService(
        fetch_data=partial(fetch_data_real, config=config),
        validate_json=validate_json_real,
        deserialize_weather_data=deserialize_weather_data_real,
    )
    weather_day_summary_report = (
        weather_service.build_weather_day_summary_report(
            station_id, api_key, date
        )
    )
    if weather_day_summary_report is None:
        print({"error" : "Error trying to get data."})
        return -2

    print("DATA API -------------------------------------------")
    print(weather_day_summary_report.model_dump_json(indent=4))
    print("\nFACEBOOK POST -------------------------------------------")
    post_content = build_post(weather_day_summary_report)
    print(post_content)
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
    args = parser.parse_args()
    config = AppConfig.from_args(args)
    return main(
        config.station_id,
        config.weather_api_key,
        previous_report_date(time_zone=config.report_timezone),
        config,
    )


if __name__ == "__main__":
    raise SystemExit(cli())
