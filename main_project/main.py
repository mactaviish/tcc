import logging
from src.utils.file_utils import airplanes, routes
from src.optimization import run_optimization

def main():
  logging.basicConfig(level=logging.WARNING, format="%(asctime)s %(levelname)s %(message)s")
  try:
    airplane_list = airplanes()
    route_list = routes()

    run_optimization(airplane_list, route_list)
  except Exception as e:
    logging.error(e)
    return

if __name__ == "__main__":
  main()
