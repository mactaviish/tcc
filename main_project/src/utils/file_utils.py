import pandas as pd
import os
from typing import Type, List, Any
from models.aircraft import Aircraft
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

def aircraft() -> List[Aircraft]:
  df = import_sheet("aircraft.xlsx")
  return df_to_object_list(df, Aircraft)

def routes() -> List[Route]:
  df = import_sheet("routes.xlsx")
  return df_to_object_list(df, Route)
