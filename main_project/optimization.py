import gurobipy as gp
from gurobipy import GRB
from typing import List
from models.airplane import Airplane
from models.route import Route
from src.utils.utils import calc_cask, calc_yield, calc_fare

def run_optimization(airplanes: List[Airplane], routes: List[Route]):
  model = gp.Model("airline_optimization")

  fare, cask, airplane_flow, passenger_count, binary, binary2, aircraft_types = create_variables(model, airplanes, routes)
  add_constraints(model, airplanes, routes, airplane_flow, passenger_count, binary, binary2, aircraft_types)

  model.setObjective(gp.quicksum(
    fare[key] * passenger_count[key] -
    cask[key] * airplane.seats * route.distance * airplane_flow[key]
    for route in routes for airplane in airplanes
    for key in [(route.destination, airplane.model)]
  ), GRB.MAXIMIZE)

  model.optimize()

def create_variables(model, airplanes, routes):
  T, C, F, P, BIN, BIN2, K = {}, {}, {}, {}, {}, {}, 3

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

  return T, C, F, P, BIN, BIN2, K

def add_constraints(model, airplanes, routes, F, P, BIN, BIN2, K):
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

# (3.5, 3.7)
  for route in routes:
    for airplane in airplanes:
      key = (route.destination, airplane.model)
      model.addConstr(F[key] <= 100 * BIN[key], name=f"link_F_BIN_{key}")
      model.addConstr(F[key] <= 100 * BIN2[airplane.model], name=f"link_F_BIN2_{key}")
      model.addConstr(P[key] <= airplane.seats * F[key], name=f"capacity_{key}")

# (3.6)
  model.addConstr(gp.quicksum(BIN2[airplane.model] for airplane in airplanes) <= K, name="aircraft_types")

# 3.9
  for route in routes:
    model.addConstr(gp.quicksum(P[(route.destination, airplane.model)] for airplane in airplanes) == route.demand, name=f"atende_demanda_{route.destination}")
