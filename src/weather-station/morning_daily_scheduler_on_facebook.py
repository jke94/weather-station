from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from weather_station.morning_daily_scheduler_on_facebook import cli


if __name__ == "__main__":
    raise SystemExit(cli())
