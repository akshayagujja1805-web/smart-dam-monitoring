def clamp(value, minimum=0.0, maximum=100.0):
    return max(minimum, min(value, maximum))


def assess_risk(reading):
    if reading.get("sensor_status") != "OK":
        return {
            "status": "SENSOR_FAULT",
            "risk_score": None,
            "condition_score": None,
            "reasons": ["One or more sensors are unavailable"]
        }

    water_level = reading["water_level"]
    rise_rate = reading["rise_rate"]
    seepage = reading["seepage"]
    tilt = reading["tilt"]
    vibration = reading["vibration"]

    # Convert individual measurements into risks from 0 to 100.
    level_risk = clamp(water_level)
    rise_risk = clamp((rise_rate / 2.0) * 100)
    seepage_risk = clamp(seepage)
    tilt_risk = clamp((tilt / 10.0) * 100)
    vibration_risk = clamp((vibration / 5.0) * 100)

    movement_risk = (tilt_risk + vibration_risk) / 2

    risk_score = (
        0.35 * level_risk
        + 0.25 * rise_risk
        + 0.20 * seepage_risk
        + 0.20 * movement_risk
    )

    risk_score = round(clamp(risk_score), 2)
    condition_score = round(100 - risk_score, 2)

    reasons = []

    if water_level >= 90:
        reasons.append("Reservoir water level is critical")
    elif water_level >= 75:
        reasons.append("Reservoir water level is high")
    elif water_level >= 60:
        reasons.append("Reservoir water level requires observation")

    if rise_rate >= 1.0:
        reasons.append("Water level is rising rapidly")
    elif rise_rate >= 0.4:
        reasons.append("Water level is gradually increasing")

    if seepage >= 60:
        reasons.append("High seepage detected")
    elif seepage >= 30:
        reasons.append("Seepage is increasing")

    if tilt >= 5:
        reasons.append("Abnormal structural tilt detected")

    if vibration >= 3:
        reasons.append("Abnormal structural vibration detected")

    combined_structural_danger = (
        seepage >= 60 and (tilt >= 5 or vibration >= 3)
    )

    high_water_danger = water_level >= 75 and rise_rate >= 1.0

    if (
        water_level >= 90
        or combined_structural_danger
        or risk_score >= 75
    ):
        status = "CRITICAL"

    elif (
        high_water_danger
        or seepage >= 60
        or tilt >= 5
        or vibration >= 3
        or risk_score >= 50
    ):
        status = "WARNING"

    elif (
        water_level >= 60
        or rise_rate >= 0.4
        or seepage >= 30
        or tilt >= 2
        or vibration >= 1
        or risk_score >= 25
    ):
        status = "WATCH"

    else:
        status = "SAFE"

    if not reasons:
        reasons.append("All monitored parameters are within normal limits")

    return {
        "status": status,
        "risk_score": risk_score,
        "condition_score": condition_score,
        "reasons": reasons
    }


if __name__ == "__main__":
    sample_reading = {
        "water_level": 80,
        "rise_rate": 1.4,
        "seepage": 82,
        "tilt": 7.5,
        "vibration": 4.0,
        "sensor_status": "OK"
    }

    result = assess_risk(sample_reading)
    print(result)