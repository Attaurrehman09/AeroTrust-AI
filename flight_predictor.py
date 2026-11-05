def predict_flight_risk(delay_minutes, weather, congestion):
    """
    Demonstration flight delay risk calculator.
    This is rule-based, not a trained machine-learning model.
    """

    score = 0

    # Existing delay
    if delay_minutes >= 60:
        score += 40
    elif delay_minutes >= 30:
        score += 25
    elif delay_minutes > 0:
        score += 10

    # Weather conditions
    weather_scores = {
        "Clear": 0,
        "Moderate": 15,
        "Severe": 30
    }

    score += weather_scores.get(weather, 0)

    # Airport congestion
    congestion_scores = {
        "Low": 0,
        "Medium": 15,
        "High": 30
    }

    score += congestion_scores.get(congestion, 0)

    score = min(score, 100)

    # Risk classification
    if score <= 30:
        level = "Low"
        color = "Green"
        recommendation = "Continue normal monitoring."

    elif score <= 60:
        level = "Medium"
        color = "Yellow"
        recommendation = "Monitor weather and airport operations."

    else:
        level = "High"
        color = "Red"
        recommendation = "Conduct operational review and prepare mitigation measures."

    return {
        "risk_score": score,
        "risk_level": level,
        "color": color,
        "recommendation": recommendation,
        "demo": True
    }