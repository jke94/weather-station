import json
import os
from pathlib import Path
from typing import Any


class PublicationStateStore:
    def __init__(self, path: str | None = None):
        configured_path = path or os.getenv(
            "WEATHER_PUBLISHING_STATE_PATH",
            ".weather_station/publishing-state.json",
        )
        self.path = Path(configured_path)
        if self.path.exists():
            state = json.loads(self.path.read_text(encoding="utf-8"))
            if not isinstance(state, dict):
                raise ValueError("Publication state must be a JSON object.")
            for record in state.values():
                if (
                    not isinstance(record, dict)
                    or record.get("status") not in {"publishing", "published"}
                    or (
                        record["status"] == "published"
                        and not isinstance(record.get("url"), str)
                    )
                ):
                    raise ValueError("Publication state contains an invalid entry.")
            self.state: dict[str, Any] = state
        else:
            self.state = {}
            self._save()

    def reserve(self, platform: str, station_id: str, date: str) -> str:
        key = self._key(platform, station_id, date)
        current = self.state.get(key)
        if current:
            return current["status"]

        self.state[key] = {"status": "publishing"}
        self._save()
        return "reserved"

    def mark_published(
        self, platform: str, station_id: str, date: str, url: str
    ) -> None:
        key = self._key(platform, station_id, date)
        if self.state.get(key, {}).get("status") != "publishing":
            raise ValueError("Publication must be reserved before completion.")

        self.state[key] = {"status": "published", "url": url}
        self._save()

    def clear_unresolved(
        self, platform: str, station_id: str, date: str
    ) -> bool:
        key = self._key(platform, station_id, date)
        if self.state.get(key, {}).get("status") != "publishing":
            return False

        del self.state[key]
        self._save()
        return True

    @staticmethod
    def _key(platform: str, station_id: str, date: str) -> str:
        if not platform or not station_id or not date:
            raise ValueError("Platform, station ID, and date are required.")
        return f"{platform}:{station_id}:{date}"

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = self.path.with_suffix(f"{self.path.suffix}.tmp")
        temporary_path.write_text(
            json.dumps(self.state, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        temporary_path.replace(self.path)
