from src.utils.file_utils import airplanes, routes, airports, valid_routes
from src.optimization import run_optimization
from src.utils.print_utils import print_map
import src.consts as consts

def main():
  consts.ROUTES_YEAR = "2024"

  airplane_list = airplanes()
  airport_list = airports()
  route_list = valid_routes(routes(), airport_list)

  scenaries = [1, 2, 3, 5, 10, 20]
  for scenary in scenaries:
    consts.AIRCRAFT_TYPE_LIMIT = scenary
    run_optimization(airplane_list, route_list, airport_list)
  print_map(routes=route_list, airports=airport_list)

if __name__ == "__main__":
  main()
