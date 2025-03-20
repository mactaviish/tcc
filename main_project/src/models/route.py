from dataclasses import dataclass

@dataclass
class Route:
  origin: str
  destination: str
  distance: float
  demand: int
