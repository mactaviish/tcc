from dataclasses import dataclass
from src.utils.str_utils import clean_string

@dataclass
class Airplane:
  manufacturer: str
  model: str
  seats: int
  range_km: float
  min_runway_length: float
  min_runway_surface: int

  def id(self):
    return clean_string(f"{self.manufacturer,self.model}")
