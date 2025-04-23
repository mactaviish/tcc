from dataclasses import dataclass
from src.utils.str_utils import clean_string

@dataclass
class Route:
  origin_city: str
  origin_state: str
  destination_city: str
  destination_state: str
  distance: float
  demand: int
  runway_length: int

  def origin_id(self) -> str:
    return clean_string(f"{self.origin_city}_{self.origin_state}")

  def destination_id(self) -> str:
    return clean_string(f"{self.destination_city}_{self.destination_state}")
