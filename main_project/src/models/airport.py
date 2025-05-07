from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Airport:
  icao_code: str
  ciad_code: str
  name: str
  city: str
  state: str
  served_city: str
  served_state: str
  lat_geo_point: float
  lon_geo_point: float
  latitude: float
  longitude: float
  altitude: float
  day_operation: str
  night_operation: str
  runway1_designation: str
  runway1_length: float
  runway1_width: float
  runway1_strength: float
  runway1_surface: str
  runway2_designation: str
  runway2_length: float
  runway2_width: float
  runway2_strength: float
  runway2_surface: str
  status: str
  registration_validity: str
  registration_decree: str
  decree_link: str

  @staticmethod
  def from_dict(d: dict) -> 'Airport':
    def to_float(val):
      try:
        return float(str(val).replace(',', '.'))
      except:
        return 0.0

    return Airport(
      icao_code             = d.get('CódigoOACI', '').strip(),
      ciad_code             = d.get('CIAD', '').strip(),
      name                  = d.get('Nome', '').strip(),
      city                  = d.get('Município', '').strip(),
      state                 = d.get('UF', '').strip(),
      served_city           = d.get('MunicípioServido', '').strip(),
      served_state          = d.get('UFServido', '').strip(),
      lat_geo_point         = to_float(d.get('LatGeoPoint')),
      lon_geo_point         = to_float(d.get('LonGeoPoint')),
      latitude              = to_float(d.get('Latitude')),
      longitude             = to_float(d.get('Longitude')),
      altitude              = to_float(d.get('Altitude')),
      day_operation         = d.get('OperaçãoDiurna', '').strip(),
      night_operation       = d.get('OperaçãoNoturna', '').strip(),
      runway1_designation   = d.get('Designação1', '').strip(),
      runway1_length        = to_float(d.get('Comprimento1')),
      runway1_width         = to_float(d.get('Largura1')),
      runway1_strength      = to_float(d.get('Resistência1')),
      runway1_surface       = d.get('Superfície1', '').strip(),
      runway2_designation   = d.get('Designação2', '').strip(),
      runway2_length        = to_float(d.get('Comprimento2')),
      runway2_width         = to_float(d.get('Largura2')),
      runway2_strength      = to_float(d.get('Resistência2')),
      runway2_surface       = d.get('Superfície2', '').strip(),
      status                = d.get('SITUAÇÃO', '').strip(),
      registration_validity = d.get('ValidadedoRegistro', '').strip(),
      registration_decree   = d.get('PortariadeRegistro', '').strip(),
      decree_link           = d.get('LinkPortaria', '').strip()
    )
