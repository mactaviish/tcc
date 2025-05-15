import pandas as pd
import src.consts as consts
import os
import json
from typing import Type, List, Dict, Any
from src.models.airplane import Airplane
from src.models.route import Route
from src.models.airport import Airport

def import_sheet(file_name) -> pd.DataFrame:
  try:
    path = os.path.join("input", file_name)
    df = pd.read_excel(path)
    return df
  except Exception as e:
    raise Exception(f"Erro ao importar a planilha '{path}': {e}")

def import_json(file_name) -> Any:
  try:    
    path = os.path.join("input", file_name)
    with open(path, "r", encoding="utf-8-sig") as f:
      return json.load(f)
  except Exception as e:
    raise Exception(f"Erro ao importar o JSON '{path}': {e}")

def df_to_object_list(df: pd.DataFrame, cls: Type) -> List[Any]:
  object_list = []
  for _, row in df.iterrows():
    obj = cls(**row.to_dict())
    object_list.append(obj)
  return object_list

def airplanes() -> List[Airplane]:
  df = import_sheet("airplanes.xlsx")
  return df_to_object_list(df, Airplane)

def routes() -> List[Route]:
  df = import_sheet("routes_2024.xlsx")
  route_list = df_to_object_list(df, Route)
  return_list = []
  for route in route_list:
    weekly_demand = round(route.demand / consts.WEEKS_YEAR)
    if weekly_demand >= consts.PAX_WEEK:
      return_list.append(
        Route(
          origin = route.origin,
          destination = route.destination,
          fare = route.fare,
          demand = weekly_demand
        )
      )
  return return_list
  # return [route for route in route_list if (route.demand > 0)]

def airports() -> Dict[str, Airport]:
  data = import_json("AerodromosPublicos.json")
  airport_list = [Airport.from_dict(entry) for entry in data]
  return { ap.icao_code: ap for ap in airport_list }

def valid_routes(routes: List[Route], airports: Dict[str, Airport]) -> List[Route]:
  valid_routes = []
  for route in routes:
    if (airports.get(route.origin) and airports.get(route.destination)):
      valid_routes.append(route)
      continue
    print(f"{route} ignored. No airport data available.")
  return valid_routes
