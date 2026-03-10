# Flask Weather App

A small Flask web app that lets a user enter a city and displays the current weather (temperature, description, and icon) using OpenWeatherMap.

## Setup

1. Create a virtual environment:

```bash
python -m venv .venv
```

2. Activate it (Windows PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Get an API key from OpenWeatherMap: https://openweathermap.org/api

5. Set your API key in the environment:

Windows PowerShell:

```powershell
$env:OPENWEATHER_API_KEY = "your_api_key_here"
```

## Run

If `python app.py` fails (e.g., `ModuleNotFoundError: No module named 'flask'`), run using the venv Python directly:

```powershell
.\.venv\Scripts\python.exe app.py
```

Then open http://127.0.0.1:5000 in your browser and enter a city name.
