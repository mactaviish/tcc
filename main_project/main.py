from src.utils.utils import get_data
from optimization import run_optimization

def main():
  airplanes, routes = get_data()
  run_optimization(airplanes, routes)
  
if __name__ == "__main__":
  main()
