"""Configuration helpers."""

from __future__ import annotations

import os
from typing import Optional


def get_env(key: str, default: Optional[str] = None) -> Optional[str]:
    return os.environ.get(key, default)


def get_openweather_api_key() -> Optional[str]:
    """Return the OpenWeatherMap API key from the environment.

    Set the key in your environment as `OPENWEATHER_API_KEY`.
    """
    return get_env("OPENWEATHER_API_KEY")


def get_openweather_base_url() -> str:
    """Return the OpenWeatherMap base URL for current weather."""
    # Using the standard current weather endpoint
    return "https://api.openweathermap.org/data/2.5/weather"
