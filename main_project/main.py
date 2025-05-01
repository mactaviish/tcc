from src.utils.file_utils import airplanes, routes, airports, valid_routes
from src.optimization import run_optimization

def main():
  airplane_list = airplanes()
  airport_list = airports()
  route_list = valid_routes(routes(), airport_list)

  run_optimization(airplane_list, route_list, airport_list)

if __name__ == "__main__":
  main()
