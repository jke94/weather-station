def calculate_risk_uv(uv:int) -> str:

    if 0 <= uv <= 2:
        return "Low"
    elif 3 <= uv <= 5:
        return "Medium"
    elif 6 <= uv <= 7:
        return "High"
    elif 8 <= uv <= 10:
        return "Very high"
    elif 11 <= uv:
        return "Extremely high"

    return "NONE"