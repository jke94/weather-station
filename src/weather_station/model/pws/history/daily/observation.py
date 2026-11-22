from model.pws.history.daily.metric import Metric
from pydantic import BaseModel

# Observation metric
class Observation(BaseModel):
    stationID: str
    tz: str
    obsTimeUtc: str
    obsTimeLocal: str
    epoch: int
    lat: float
    lon: float
    solarRadiationHigh: float
    uvHigh: float
    winddirAvg: int
    humidityHigh: float
    humidityLow: float
    humidityAvg: float
    qcStatus: int
    metric: Metric