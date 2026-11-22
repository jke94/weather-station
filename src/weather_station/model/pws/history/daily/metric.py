from pydantic import BaseModel

# Metric section
class Metric(BaseModel):
    tempHigh: float
    tempLow: float
    tempAvg: float
    windspeedHigh: float
    windspeedLow: float
    windspeedAvg: float
    windgustHigh: float
    windgustLow: float
    windgustAvg: float
    dewptHigh: float
    dewptLow: float
    dewptAvg: float
    windchillHigh: float
    windchillLow: float
    windchillAvg: float
    heatindexHigh: float
    heatindexLow: float
    heatindexAvg: float
    pressureMax: float
    pressureMin: float
    pressureTrend: float
    precipRate: float
    precipTotal: float