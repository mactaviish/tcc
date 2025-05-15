from dataclasses import dataclass

@dataclass
class Route:
  origin: str
  destination: str
  fare: float
  demand: int
