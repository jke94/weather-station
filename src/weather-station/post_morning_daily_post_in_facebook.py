from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from weather_station.post_morning_daily_post_in_facebook import cli


if __name__ == "__main__":
    raise SystemExit(cli())
