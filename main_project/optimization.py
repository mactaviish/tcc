import gurobipy as gp
import sys
from gurobipy import GRB, Model
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
  T, C, F, P, BIN, BIN2, K, Z = {}, {}, {}, {}, {}, {}, 2, sys.maxsize

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
    print(f"\nValor objetivo: {model.ObjVal}\n")
    print("Solução ótima encontrada.")
    for key, var in F.items():
        if var.X > 0:
            print(f"Destino: {key[0]} | Aeronave: {key[1]}")
            print(f"  Aeronaves: {F[key].X}")
            print(f"  Passageiros: {P[key].X}")
            print(f"  BIN (rota ativa): {BIN[key].X}")
            print(f"  BIN2 (modelo usado): {BIN2[key[1]].X}\n")
  else:
      print("Nenhuma solução ótima foi encontrada.")
