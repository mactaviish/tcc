from dataclasses import dataclass

@dataclass
class Route:
  origin: str
  destination: str
  demand: int
