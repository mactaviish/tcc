import pandas as pd
import os
from typing import Type, List, Any
from models.airplane import Airplane
from models.route import Route

def import_sheet(file_name) -> pd.DataFrame:
  try:
    path = os.path.join("input", file_name)
    df = pd.read_excel(path)
    return df
  except Exception as e:
    raise Exception(f"Erro ao importar a planilha '{path}': {e}")

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
  df = import_sheet("routes.xlsx")
  route_list = df_to_object_list(df, Route)
  # return [route for route in route_list if route.origin == "Chapecó - SC"]
  return route_list
