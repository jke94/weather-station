from model.pws.history.daily.observation import Observation
from pydantic import BaseModel
from typing import List

class WeatherResponse(BaseModel):
    observations: List[Observation]