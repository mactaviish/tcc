from dataclasses import dataclass
from utils.str_utils import clean_string

@dataclass
class Airplane:
  manufacturer: str
  model: str
  seats: int
  range_km: float
  min_runway_length: float

  def id(self):
    return clean_string(f"{self.model}")
