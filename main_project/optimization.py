import gurobipy as gp
import csv
from gurobipy import GRB, Model
from tabulate import tabulate
from typing import List
from models.airplane import Airplane
from models.route import Route
from src.utils.utils import calc_cask, calc_yield, calc_fare

def run_optimization(airplanes: List[Airplane], routes: List[Route]):
  model = gp.Model("airline_optimization")

  fare, cask, airplane_flow, passenger_count, binary, binary2, aircraft_types, max_fleet_qtd = create_variables(model, airplanes, routes)
  add_constraints(model, airplanes, routes, airplane_flow, passenger_count, binary, binary2, aircraft_types, max_fleet_qtd)

  model.setObjective(gp.quicksum(
    (fare[(route.destination_id(), airplane.id())] * passenger_count[(route.destination_id(), airplane.id())]) -
    (cask[(route.destination_id(), airplane.id())] * airplane.seats * route.distance * airplane_flow[(route.destination_id(), airplane.id())])
    for route in routes for airplane in airplanes
  ), GRB.MAXIMIZE)

  model.setParam(GRB.Param.TimeLimit, 600)
  model.optimize()

  print_solution(model, airplane_flow, passenger_count, binary, binary2)

def create_variables(model: Model, airplanes: List[Airplane], routes: List[Route]):
  T, C, F, P, BIN, BIN2, K, Z = {}, {}, {}, {}, {}, {}, 10, 100

  for route in routes:
    for airplane in airplanes:
      key = (route.destination_id(), airplane.id())
      T[key] = calc_fare(route.distance)
      C[key] = calc_cask(airplane.seats, route.distance)
      F[key] = model.addVar(vtype=GRB.INTEGER, name=f"F_{key}")
      P[key] = model.addVar(vtype=GRB.INTEGER, name=f"P_{key}")
      BIN[key] = model.addVar(vtype=GRB.BINARY, name=f"BIN_{key}")

  for airplane in airplanes:
    BIN2[airplane.id()] = model.addVar(vtype=GRB.BINARY, name=f"BIN2_{airplane.id()}")

  return T, C, F, P, BIN, BIN2, K, Z

def add_constraints(model: Model, airplanes: List[Airplane], routes: List[Route], F, P, BIN, BIN2, K, Z):
# (3.2)
  total_capacity = {
    route.destination_id(): gp.quicksum(
      airplane.seats * F[(route.destination_id(), airplane.id())]
      for airplane in airplanes
    ) for route in routes
  }
  for route in routes:
    model.addConstr(total_capacity[route.destination_id()] >= route.demand, name=f"demand_{route.destination_id()}")

# (3.3)
  for route in routes:
    for airplane in airplanes:
      key = (route.destination_id(), airplane.id())
      model.addConstr(airplane.min_runway_length * BIN[key] <= route.runway_length, name=f"runway_{key}")

# (3.4)
  for route in routes:
    for airplane in airplanes:
      key = (route.destination_id(), airplane.id())
      model.addConstr(airplane.range_km >= route.distance * BIN[key], name=f"range_{key}")

# (3.5, 3.7, 3.10)
  for route in routes:
    for airplane in airplanes:
      key = (route.destination_id(), airplane.id())
      model.addConstr(F[key] <= Z * BIN[key], name=f"link_F_BIN_{key}")
      model.addConstr(F[key] <= Z * BIN2[airplane.id()], name=f"link_F_BIN2_{key}")
      model.addConstr(P[key] <= airplane.seats * F[key], name=f"capacity_{key}")
      model.addConstr(P[key] >= 0, name=f"non_negativity_passenger_{key}")
      model.addConstr(F[key] >= 0, name=f"non_negativity_fleet_flow_{key}")

# (3.6, 3.9)
  for route in routes:
    model.addConstr(gp.quicksum(BIN[route.destination_id(), airplane.id()] for airplane in airplanes) <= K, name=f"aircraft_types_{route.origin_id()}_{route.destination_id()}")
    model.addConstr(gp.quicksum(P[(route.destination_id(), airplane.id())] for airplane in airplanes) == route.demand, name=f"meet_demand_{route.origin_id()}_{route.destination_id()}")

# (3.8)
  model.addConstr(gp.quicksum(BIN2[airplane.id()] for airplane in airplanes) <= K, name=f"aircraft_types")

def print_solution(model: Model, F, P, BIN, BIN2):
  if model.status == gp.GRB.OPTIMAL:
    print("Solução ótima encontrada.\n")
    print(f"\nValor objetivo: {model.ObjVal}\n")

    table_data = []
    headers = ["Destination", "Airplane", "Flow", "Passengers", "Active Route", "Active Airplane"]
    for key, var in F.items():
        if var.X > 0:
          destination, airplane = key
          active_route = "Yes" if BIN[key].X >= 0.5 else "No"
          active_airplane = "Yes" if BIN2[airplane].X >= 0.5 else "No"
          row = [
            destination,
            airplane,
            F[key].X,
            P[key].X,
            active_route,
            active_airplane
          ]
          table_data.append(row)
    print(tabulate(table_data, headers, tablefmt="fancy_grid"))
    with open("./output/solution.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(table_data)
  else:
      print("Nenhuma solução ótima foi encontrada.")
