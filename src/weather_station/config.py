import argparse
from dataclasses import dataclass
import math
import os
from typing import Mapping
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from dotenv import load_dotenv

DEFAULT_REPORT_TIME_ZONE = "Europe/Madrid"
DEFAULT_WEATHER_REQUEST_TIMEOUT_SECONDS = 15.0
DEFAULT_WEATHER_REQUEST_RETRIES = 3
DEFAULT_PUBLISHING_STATE_PATH = ".weather_station/publishing-state.json"

CLI_ARGUMENT_ENV = {
    "weather_underground_station_id": "WEATHER_UNDERGROUND_STATION_ID",
    "weather_underground_api_key": "WEATHER_UNDERGROUND_API_KEY",
    "x_api_key": "X_API_KEY",
    "x_api_key_secret": "X_API_KEY_SECRET",
    "x_access_token": "X_ACCESS_TOKEN",
    "x_access_secret_token": "X_ACCESS_SECRET_TOKEN",
    "facebook_access_token": "FACEBOOK_ACCESS_TOKEN",
    "facebook_page_id": "FACEBOOK_PAGE_ID",
}


@dataclass(frozen=True)
class AppConfig:
    station_id: str | None
    weather_api_key: str | None
    x_api_key: str | None
    x_api_key_secret: str | None
    x_access_token: str | None
    x_access_secret_token: str | None
    facebook_access_token: str | None
    facebook_page_id: str | None
    report_timezone: str
    weather_request_timeout_seconds: float
    weather_request_retries: int
    publishing_state_path: str

    @classmethod
    def from_args(
        cls,
        args: argparse.Namespace,
        environ: Mapping[str, str] | None = None,
    ) -> "AppConfig":
        cli_values = {
            environment_name: getattr(args, argument_name, None)
            for argument_name, environment_name in CLI_ARGUMENT_ENV.items()
        }
        return cls.from_sources(cli_values, environ)

    @classmethod
    def from_sources(
        cls,
        cli_values: Mapping[str, str | None] | None = None,
        environ: Mapping[str, str] | None = None,
    ) -> "AppConfig":
        if environ is None:
            load_dotenv()
            source = os.environ
        else:
            source = environ

        cli_values = cli_values or {}

        def value(name: str) -> str | None:
            return cli_values.get(name) or source.get(name)

        report_timezone = (
            value("REPORT_TIME_ZONE") or DEFAULT_REPORT_TIME_ZONE
        )
        try:
            ZoneInfo(report_timezone)
        except ZoneInfoNotFoundError as error:
            raise ValueError(
                f"Unknown report time zone: {report_timezone}"
            ) from error

        try:
            request_timeout = float(
                value("WEATHER_REQUEST_TIMEOUT_SECONDS")
                or DEFAULT_WEATHER_REQUEST_TIMEOUT_SECONDS
            )
            request_retries = int(
                value("WEATHER_REQUEST_RETRIES")
                or DEFAULT_WEATHER_REQUEST_RETRIES
            )
        except ValueError as error:
            raise ValueError(
                "Weather request timeout and retries must be numeric."
            ) from error

        if not math.isfinite(request_timeout) or request_timeout <= 0:
            raise ValueError("Weather request timeout must be greater than 0.")
        if request_retries < 0:
            raise ValueError("Weather request retries cannot be negative.")

        return cls(
            station_id=value("WEATHER_UNDERGROUND_STATION_ID"),
            weather_api_key=value("WEATHER_UNDERGROUND_API_KEY"),
            x_api_key=value("X_API_KEY"),
            x_api_key_secret=value("X_API_KEY_SECRET"),
            x_access_token=value("X_ACCESS_TOKEN"),
            x_access_secret_token=value("X_ACCESS_SECRET_TOKEN"),
            facebook_access_token=value("FACEBOOK_ACCESS_TOKEN"),
            facebook_page_id=value("FACEBOOK_PAGE_ID"),
            report_timezone=report_timezone,
            weather_request_timeout_seconds=request_timeout,
            weather_request_retries=request_retries,
            publishing_state_path=(
                value("WEATHER_PUBLISHING_STATE_PATH")
                or DEFAULT_PUBLISHING_STATE_PATH
            ),
        )
