
def calculate_wind_direction(wind_direction_avg:int) -> str:

    wind_directions = [
        "N", 
        "NNE", 
        "NE", 
        "ENE",
        "E", 
        "ESE", 
        "SE", 
        "SSE",
        "S", 
        "SSW", 
        "SW", 
        "WSW", 
        "W", 
        "WNW", 
        "NW", 
        "NNW"
    ]
    
    wind_direction = wind_directions[int((wind_direction_avg % 360) / 22.5)]

    return wind_direction