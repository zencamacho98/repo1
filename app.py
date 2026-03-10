"""Flask app to display current weather for a given city."""

from __future__ import annotations

from flask import Flask, jsonify, render_template, request, send_from_directory

from weather import WeatherError, get_current_weather


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["TEMPLATES_AUTO_RELOAD"] = True

    @app.route("/", methods=["GET"])
    def index():
        # Show the form and optionally weather data if provided via query params
        return render_template("index.html")

    @app.route("/weather", methods=["POST"])
    def weather():
        city = request.form.get("city", "").strip()
        if not city:
            return render_template(
                "index.html", error="Please enter a city name."  # type: ignore[arg-type]
            )

        try:
            weather_data = get_current_weather(city)
        except WeatherError as exc:
            return render_template("index.html", error=str(exc))

        return render_template("index.html", weather=weather_data)

    # Calculator UI + API (served from the same Flask app)
    @app.route("/calculator", methods=["GET"])
    def calculator():
        return send_from_directory("static", "index.html")

    @app.route("/api/calc", methods=["POST"])
    def calc_api():
        payload = request.get_json(silent=True) or {}
        expression = payload.get("expression", "")

        if not isinstance(expression, str):
            return jsonify({"detail": "expression must be a string"}), 400

        try:
            # The calculator logic is shared via `calc_core.py`.
            from calc_core import evaluate_expression

            result = evaluate_expression(expression)
        except Exception as exc:
            return jsonify({"detail": str(exc)}), 400

        return jsonify({"result": result})

    return app


# Provide an application instance for both `python app.py` and `flask run`.
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
