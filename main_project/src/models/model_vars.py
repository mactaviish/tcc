from dataclasses import dataclass

@dataclass
class ModelVars:
  D: dict     # distance
  T: dict     # fare
  C: dict     # cask
  F: dict     # airplane_flow
  P: dict     # passenger_count
  BIN: dict   # route_active
  BIN2: dict  # airplane_active
  K: int      # aircraft_types
  Z: int      # max_fleet_qtd
