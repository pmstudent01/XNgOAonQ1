"""Application configuration.

Values are read from environment variables (optionally loaded from a local
``.env`` file) so the same app can target the local mock, a staging server, or
production without code changes.
"""

from __future__ import annotations

import os
from dataclasses import dataclass


def _load_dotenv() -> None:
    """Best-effort load of a local .env file without a hard dependency.

    If ``python-dotenv`` is installed it is used; otherwise a minimal parser
    reads KEY=VALUE lines from a ``.env`` file in the current working dir.
    """
    try:
        from dotenv import load_dotenv  # type: ignore

        load_dotenv()
        return
    except Exception:
        pass

    path = os.path.join(os.getcwd(), ".env")
    if not os.path.isfile(path):
        return
    try:
        with open(path, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                os.environ.setdefault(key, value)
    except OSError:
        pass


@dataclass(frozen=True)
class Settings:
    """Runtime settings for the Vehicle Service app."""

    base_url: str
    api_key: str | None
    timeout: float

    @classmethod
    def from_env(cls) -> "Settings":
        _load_dotenv()
        return cls(
            # Default matches the "Local - Agent Mode" Postman environment.
            base_url=os.getenv("VEHICLE_SERVICE_BASE_URL", "http://localhost:4501"),
            api_key=os.getenv("VEHICLE_SERVICE_API_KEY") or None,
            timeout=float(os.getenv("VEHICLE_SERVICE_TIMEOUT", "30")),
        )
