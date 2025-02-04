from pydantic import BaseModel

class WeatherDaySummaryReport(BaseModel):
    Date: str
    TemperatureHigh: float
    TemperatureAvg: float
    TemperatureLow: float
    DewPointHigh: float
    DewPointLow: float
    DewPointAvg: float
    HumidityHigh: float
    HumidityLow: float
    HumidityAvg: float
    PrecipitationTotal: float
    PressureMax: float
    PressureMin: float
    WindSpeedHigh: float
    WindSpeedAvg: float
    WindGustHigh: float
    WindGustAvg: float
    WindDirectionAvg: str
    UvHighRisk: str
    UvIndexHigh: float
    SolarRadiationHigh: float