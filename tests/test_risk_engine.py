from dashboard.prediction import predict_water_level
from dashboard.risk_engine import assess_risk


def test_normal_condition_is_safe():
    reading = {
        "water_level": 40,
        "rise_rate": 0.1,
        "seepage": 5,
        "tilt": 0.3,
        "vibration": 0.1,
        "sensor_status": "OK"
    }

    result = assess_risk(reading)

    assert result["status"] == "SAFE"
    assert result["condition_score"] > 75


def test_rapid_rise_generates_warning():
    reading = {
        "water_level": 78,
        "rise_rate": 1.5,
        "seepage": 10,
        "tilt": 0.5,
        "vibration": 0.3,
        "sensor_status": "OK"
    }

    result = assess_risk(reading)

    assert result["status"] == "WARNING"
    assert "Water level is rising rapidly" in result["reasons"]


def test_combined_structural_problem_is_critical():
    reading = {
        "water_level": 75,
        "rise_rate": 1.0,
        "seepage": 80,
        "tilt": 7,
        "vibration": 4,
        "sensor_status": "OK"
    }

    result = assess_risk(reading)

    assert result["status"] == "CRITICAL"
    assert "High seepage detected" in result["reasons"]


def test_prediction_calculates_time_to_critical():
    reading = {
        "water_level": 75,
        "rise_rate": 1.5,
        "sensor_status": "OK"
    }

    result = predict_water_level(reading)

    assert result["trend"] == "RISING_RAPIDLY"
    assert result["predicted_level_10_min"] == 90
    assert result["minutes_to_critical"] == 10


def test_sensor_fault_disables_assessment_and_prediction():
    reading = {
        "sensor_status": "FAULT"
    }

    assessment = assess_risk(reading)
    prediction = predict_water_level(reading)

    assert assessment["status"] == "SENSOR_FAULT"
    assert assessment["condition_score"] is None
    assert prediction["trend"] == "UNKNOWN"
    assert prediction["minutes_to_critical"] is None