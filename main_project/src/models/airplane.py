from dataclasses import dataclass

@dataclass
class Airplane:
  manufacturer: str
  model: str
  seats: int
  range_km: float
  min_runway_length: float
