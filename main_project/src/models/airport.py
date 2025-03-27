from dataclasses import dataclass
from typing import List

@dataclass
class Runway:
  designation: str
  length: float

@dataclass
class Airport:
  icao: str
  city: str
  name: str
  distance: float
  demand: int
  runways: List[Runway]
