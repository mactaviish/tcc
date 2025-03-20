import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.utils.utils import get_data, calc_cask, calc_yield, calc_fare

def main():
  aircraft, routes = get_data()
  
  for airplane in aircraft:
    print(airplane)

  for route in routes:
    print(route)

if __name__ == "__main__":
  main()
