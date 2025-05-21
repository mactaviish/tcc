import gurobipy as gp
import src.consts as consts
import csv
from gurobipy import GRB, Model
from tabulate import tabulate
from typing import List, Dict
from src.models.model_vars import ModelVars
from src.models.airplane import Airplane
from src.models.route import Route
from src.models.airport import Airport
from src.utils.utils import calc_cask, calc_distance

def run_optimization(airplanes: List[Airplane], routes: List[Route], airports: Dict[str, Airport]):
  model = gp.Model("airline_optimization")

  variables = create_variables(model, airplanes, routes, airports)
  add_constraints(model, airplanes, routes, airports, variables)

  model.setObjective(gp.quicksum(
    (variables.T[(route.destination, airplane.id())] * variables.P[(route.destination, airplane.id())]) -
    (variables.C[(route.destination, airplane.id())] * airplane.seats * variables.D[route.origin, route.destination] * variables.F[(route.destination, airplane.id())])
    for route in routes for airplane in airplanes
  ), GRB.MAXIMIZE)

  model.setParam(GRB.Param.LogToConsole, 0)
  model.setParam(GRB.Param.LogFile, "./output/gurobi.log")
  model.setParam(GRB.Param.TimeLimit, consts.TIME_LIMIT)
  model.optimize()

  print_solution(model, variables)

def create_variables(model: Model, airplanes: List[Airplane], routes: List[Route], airports: Dict[str, Airport]) -> ModelVars:
  D, T, C, F, P, BIN, BIN2, K, Z = {}, {}, {}, {}, {}, {}, {}, consts.AIRCRAFT_TYPE_LIMIT, consts.MAX_FLIGHTS_PER_ROUTE

  for route in routes:
    D[route.origin, route.destination] = calc_distance(airports.get(route.origin), airports.get(route.destination))
    for airplane in airplanes:
      key = (route.destination, airplane.id())
      T[key] = route.fare
      C[key] = calc_cask(airplane.seats, D[route.origin, route.destination])
      F[key] = model.addVar(vtype=GRB.INTEGER, name=f"F_{key}")
      P[key] = model.addVar(vtype=GRB.INTEGER, name=f"P_{key}")
      BIN[key] = model.addVar(vtype=GRB.BINARY, name=f"BIN_{key}")

  for airplane in airplanes:
    BIN2[airplane.id()] = model.addVar(vtype=GRB.BINARY, name=f"BIN2_{airplane.id()}")

  return ModelVars(D, T, C, F, P, BIN, BIN2, K, Z)

def add_constraints(model: Model, airplanes: List[Airplane], routes: List[Route], airports: Dict[str, Airport], variables: ModelVars):
# (3.2)
  total_capacity = {
    route.destination: gp.quicksum(
      airplane.seats * variables.F[(route.destination, airplane.id())]
      for airplane in airplanes
    ) for route in routes
  }
  for route in routes:
    model.addConstr(total_capacity[route.destination] >= route.demand, name=f"demand_{route.destination}")

# (3.3)
  for route in routes:
    for airplane in airplanes:
      key = (route.destination, airplane.id())
      airport = airports.get(route.destination)
      runway_details = [
        (airport.runway1_length, airport.runway1_surface),
        (airport.runway2_length, airport.runway2_surface)
      ]
      larger_runway_length, larger_runway_surface = max(runway_details)

      model.addConstr(airplane.min_runway_length * variables.BIN[key] <= larger_runway_length, name=f"runway_length_{key}")
      model.addConstr(airplane.min_runway_surface * variables.BIN[key] <= larger_runway_surface, name=f"runway_surface_{key}")

# (3.4)
  for route in routes:
    for airplane in airplanes:
      key = (route.destination, airplane.id())
      model.addConstr(airplane.range_km >= variables.D[route.origin, route.destination] * variables.BIN[key], name=f"range_{key}")

# (3.5, 3.7, 3.10)
  for route in routes:
    for airplane in airplanes:
      key = (route.destination, airplane.id())
      model.addConstr(variables.F[key] <= variables.Z * variables.BIN[key], name=f"link_F_BIN_{key}")
      model.addConstr(variables.F[key] <= variables.Z * variables.BIN2[airplane.id()], name=f"link_F_BIN2_{key}")
      model.addConstr(variables.P[key] <= airplane.seats * variables.F[key], name=f"capacity_{key}")
      model.addConstr(variables.P[key] >= 0, name=f"non_negativity_passenger_{key}")
      model.addConstr(variables.F[key] >= 0, name=f"non_negativity_fleet_flow_{key}")

# (3.6, 3.9)
  for route in routes:
    model.addConstr(gp.quicksum(variables.BIN[route.destination, airplane.id()] for airplane in airplanes) <= variables.K, name=f"aircraft_types_{route.origin}_{route.destination}")
    model.addConstr(gp.quicksum(variables.P[(route.destination, airplane.id())] for airplane in airplanes) == route.demand, name=f"meet_demand_{route.origin}_{route.destination}")

# (3.8)
  model.addConstr(gp.quicksum(variables.BIN2[airplane.id()] for airplane in airplanes) <= variables.K, name=f"aircraft_types")

def print_solution(model: Model, variables: ModelVars):
  if model.status == gp.GRB.OPTIMAL:
    print("\nSolução ótima encontrada.")
    print(f"\nValor objetivo: {model.ObjVal}\n")

    table_data = []
    headers = ["Destination", "Airplane", "Flow", "Passengers", "Active Route", "Active Airplane"]
    for key, var in variables.F.items():
        if var.X > 0:
          destination, airplane = key
          active_route = "Yes" if variables.BIN[key].X >= 0.5 else "No"
          active_airplane = "Yes" if variables.BIN2[airplane].X >= 0.5 else "No"
          row = [
            destination,
            airplane,
            variables.F[key].X,
            variables.P[key].X,
            active_route,
            active_airplane
          ]
          table_data.append(row)
    table_data.append([
      "Valor objetivo",
      model.ObjVal
    ])
    print(tabulate(table_data, headers, tablefmt="fancy_grid"))
    with open(f"./output/{consts.AIRCRAFT_TYPE_LIMIT}.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(table_data)
  else:
      print("Nenhuma solução ótima foi encontrada.")
