import numpy as np
import math
import src.consts as consts
from src.models.airport import Airport
from typing import Tuple

def calc_cask(seats: int, distance: float):
  return np.exp(consts.LN_KC + consts.BETA1 * np.log(seats) + consts.BETA2 * np.log(distance))

def calc_distance(a1: Airport, a2: Airport) -> float:
  coord1 = (a1.lat_geo_point, a1.lon_geo_point)
  coord2 = (a2.lat_geo_point, a2.lon_geo_point)
  return round(haversine_distance(coord1, coord2), 1)

def haversine_distance(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
  lat1, lon1 = coord1
  lat2, lon2 = coord2

  phi1, phi2 = math.radians(lat1), math.radians(lat2)
  dphi = math.radians(lat2 - lat1)
  dlambda = math.radians(lon2 - lon1)

  a = math.sin(dphi / 2) ** 2 + \
      math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
  return 2 * consts.EARTH_RADIUS * math.atan2(math.sqrt(a), math.sqrt(1 - a))
