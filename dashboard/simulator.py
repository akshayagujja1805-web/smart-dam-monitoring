import random
from datetime import datetime


SCENARIOS = {
    "normal": {
        "water_level": 40.0,
        "rise_rate": 0.1,
        "seepage": 5.0,
        "tilt": 0.3,
        "vibration": 0.1
    },
    "gradual_rise": {
        "water_level": 60.0,
        "rise_rate": 0.4,
        "seepage": 8.0,
        "tilt": 0.4,
        "vibration": 0.2
    },
    "rapid_rise": {
        "water_level": 76.0,
        "rise_rate": 1.5,
        "seepage": 12.0,
        "tilt": 0.5,
        "vibration": 0.3
    },
    "critical_level": {
        "water_level": 94.0,
        "rise_rate": 2.0,
        "seepage": 18.0,
        "tilt": 0.8,
        "vibration": 0.4
    },
    "seepage_problem": {
        "water_level": 58.0,
        "rise_rate": 0.2,
        "seepage": 78.0,
        "tilt": 0.5,
        "vibration": 0.3
    },
    "structural_problem": {
        "water_level": 55.0,
        "rise_rate": 0.2,
        "seepage": 15.0,
        "tilt": 7.0,
        "vibration": 3.5
    },
    "combined_danger": {
        "water_level": 80.0,
        "rise_rate": 1.4,
        "seepage": 82.0,
        "tilt": 7.5,
        "vibration": 4.0
    }
}


def generate_reading(scenario="normal"):
    if scenario not in SCENARIOS:
        raise ValueError(f"Unknown scenario: {scenario}")

    base = SCENARIOS[scenario]

    return {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "scenario": scenario,
        "water_level": round(base["water_level"] + random.uniform(-1, 1), 2),
        "rise_rate": round(base["rise_rate"] + random.uniform(-0.05, 0.05), 2),
        "seepage": round(base["seepage"] + random.uniform(-2, 2), 2),
        "tilt": round(base["tilt"] + random.uniform(-0.1, 0.1), 2),
        "vibration": round(base["vibration"] + random.uniform(-0.1, 0.1), 2),
        "sensor_status": "OK"
    }


if __name__ == "__main__":
    reading = generate_reading("normal")
    print(reading)
