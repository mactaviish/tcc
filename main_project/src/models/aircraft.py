from dataclasses import dataclass

@dataclass
class Aircraft:
  manufacturer: str
  model: str
  seats: int
  range_km: float
  min_runway_length: float
