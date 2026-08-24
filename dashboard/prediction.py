def clamp(value, minimum=0.0, maximum=100.0):
    return max(minimum, min(value, maximum))


def predict_water_level(reading, critical_level=90.0):
    if reading.get("sensor_status") != "OK":
        return {
            "trend": "UNKNOWN",
            "predicted_level_10_min": None,
            "predicted_level_30_min": None,
            "minutes_to_critical": None,
            "message": "Prediction unavailable because of a sensor fault"
        }

    current_level = reading["water_level"]
    rise_rate = reading["rise_rate"]

    predicted_10 = clamp(current_level + rise_rate * 10)
    predicted_30 = clamp(current_level + rise_rate * 30)

    if current_level >= critical_level:
        trend = "CRITICAL"
        minutes_to_critical = 0
        message = "The reservoir is already at or above the critical level"

    elif rise_rate >= 1.0:
        trend = "RISING_RAPIDLY"
        minutes_to_critical = round(
            (critical_level - current_level) / rise_rate,
            2
        )
        message = (
            f"Critical level may be reached in approximately "
            f"{minutes_to_critical} minutes"
        )

    elif rise_rate > 0.15:
        trend = "RISING_SLOWLY"
        minutes_to_critical = round(
            (critical_level - current_level) / rise_rate,
            2
        )
        message = (
            f"Water level is rising slowly. Critical level may be "
            f"reached in approximately {minutes_to_critical} minutes"
        )

    elif rise_rate < -0.15:
        trend = "FALLING"
        minutes_to_critical = None
        message = "Water level is currently falling"

    else:
        trend = "STABLE"
        minutes_to_critical = None
        message = "No developing high-water condition detected"

    return {
        "trend": trend,
        "predicted_level_10_min": round(predicted_10, 2),
        "predicted_level_30_min": round(predicted_30, 2),
        "minutes_to_critical": minutes_to_critical,
        "message": message
    }


if __name__ == "__main__":
    sample_reading = {
        "water_level": 76.0,
        "rise_rate": 1.5,
        "sensor_status": "OK"
    }

    result = predict_water_level(sample_reading)
    print(result)