from flask import Flask, jsonify, request

from risk_engine import assess_risk
from simulator import SCENARIOS, generate_reading


app = Flask(__name__)


@app.route("/")
def home():
    return jsonify(
        {
            "project": "Smart Dam Safety Monitoring System",
            "status": "Software setup completed",
            "mode": "Simulation"
        }
    )


@app.route("/api/scenarios")
def get_scenarios():
    return jsonify({"scenarios": list(SCENARIOS.keys())})


@app.route("/api/readings")
def get_readings():
    scenario = request.args.get("scenario", "normal")

    try:
        reading = generate_reading(scenario)
        assessment = assess_risk(reading)

        return jsonify(
            {
                "reading": reading,
                "assessment": assessment
            }
        )

    except ValueError as error:
        return jsonify({"error": str(error)}), 400


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)