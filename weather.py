"""Weather API integration."""

from __future__ import annotations

from typing import Any, Dict, Optional

import requests

from config import get_openweather_api_key, get_openweather_base_url


class WeatherError(Exception):
    pass


def get_current_weather(city: str) -> Dict[str, Any]:
    """Return a dict with current weather info for a given city.

    Raises:
        WeatherError: If the city is invalid, API key missing, or the API request fails.
    """

    api_key = get_openweather_api_key()
    if not api_key:
        raise WeatherError("Missing OPENWEATHER_API_KEY environment variable.")

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
    }

    resp = requests.get(get_openweather_base_url(), params=params, timeout=10)
    if resp.status_code != 200:
        try:
            data = resp.json()
            message = data.get("message") or resp.reason
        except Exception:
            message = resp.text or resp.reason
        raise WeatherError(f"Weather API error: {message}")

    data = resp.json()

    # Extract useful fields
    name = data.get("name") or city
    sys = data.get("sys") or {}
    country = sys.get("country", "")
    main = data.get("main") or {}
    weather_list = data.get("weather") or []
    weather = weather_list[0] if weather_list else {}

    icon = weather.get("icon")
    icon_url = (
        f"https://openweathermap.org/img/wn/{icon}@2x.png" if icon else ""
    )

    return {
        "city": name,
        "country": country,
        "temperature_c": main.get("temp"),
        "description": weather.get("description"),
        "icon_url": icon_url,
    }
