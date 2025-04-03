import gurobipy as gp
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
    (fare[(route.destination, airplane.model)] * passenger_count[(route.destination, airplane.model)]) -
    (cask[(route.destination, airplane.model)] * airplane.seats * route.distance * airplane_flow[(route.destination, airplane.model)])
    for route in routes for airplane in airplanes
  ), GRB.MAXIMIZE)

  model.setParam(GRB.Param.TimeLimit, 600)
  model.optimize()

  print_solution(model)

def create_variables(model: Model, airplanes: List[Airplane], routes: List[Route]):
  T, C, F, P, BIN, BIN2, K, Z = {}, {}, {}, {}, {}, {}, 7, 100

  for route in routes:
    for airplane in airplanes:
      key = (route.destination, airplane.model)
      T[key] = calc_fare(route.distance)
      C[key] = calc_cask(airplane.seats, route.distance)
      F[key] = model.addVar(vtype=GRB.INTEGER, name=f"F_{key}")
      P[key] = model.addVar(vtype=GRB.INTEGER, name=f"P_{key}")
      BIN[key] = model.addVar(vtype=GRB.BINARY, name=f"BIN_{key}")

  for airplane in airplanes:
    BIN2[airplane.model] = model.addVar(vtype=GRB.BINARY, name=f"BIN2_{airplane.model}")

  return T, C, F, P, BIN, BIN2, K, Z

def add_constraints(model: Model, airplanes: List[Airplane], routes: List[Route], F, P, BIN, BIN2, K, Z):
# (3.2)
  total_capacity = {
    route.destination: gp.quicksum(
      airplane.seats * F[(route.destination, airplane.model)]
      for airplane in airplanes
    ) for route in routes
  }
  for route in routes:
    model.addConstr(total_capacity[route.destination] >= route.demand, name=f"demand_{route.destination}")

# (3.3)
  for route in routes:
    for airplane in airplanes:
      key = (route.destination, airplane.model)
      model.addConstr(airplane.min_runway_length * BIN[key] <= route.runway_length, name=f"runway_{key}")

# (3.4)
  for route in routes:
    for airplane in airplanes:
      key = (route.destination, airplane.model)
      model.addConstr(airplane.range_km >= route.distance * BIN[key], name=f"range_{key}")

# (3.5, 3.7, 3.10)
  for route in routes:
    for airplane in airplanes:
      key = (route.destination, airplane.model)
      model.addConstr(F[key] <= Z * BIN[key], name=f"link_F_BIN_{key}")
      model.addConstr(F[key] <= Z * BIN2[airplane.model], name=f"link_F_BIN2_{key}")
      model.addConstr(P[key] <= airplane.seats * F[key], name=f"capacity_{key}")

# (3.6, 3.9)
  for route in routes:
    model.addConstr(gp.quicksum(BIN[route.destination, airplane.model] for airplane in airplanes) <= K, name=f"aircraft_types_{route.origin}_{route.destination}")
    model.addConstr(gp.quicksum(P[(route.destination, airplane.model)] for airplane in airplanes) == route.demand, name=f"meet_demand_{route.origin}_{route.destination}")

# (3.8)
  model.addConstr(gp.quicksum(BIN2[airplane.model] for airplane in airplanes) <= K, name=f"aircraft_types")

def print_solution(model: Model):
  # model.write("./output/solution.sol")
  model.write('./output/model.mps')
  model.write('./output/model.lp')
  model.computeIIS()
  model.write("./output/model.ilp")
