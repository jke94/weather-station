from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from weather_station.config import DEFAULT_REPORT_TIME_ZONE


def previous_report_date(
    now: datetime | None = None,
    time_zone: str = DEFAULT_REPORT_TIME_ZONE,
) -> str:
    report_time_zone = ZoneInfo(time_zone)
    current_time = now or datetime.now(report_time_zone)
    if current_time.tzinfo is None:
        raise ValueError("now must be timezone-aware")

    report_date = current_time.astimezone(report_time_zone).date()
    return (report_date - timedelta(days=1)).strftime("%Y%m%d")
