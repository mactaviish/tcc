import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.utils.utils import get_data
from optimization import run_optimization

def main():
  airplanes, routes = get_data()
  run_optimization(airplanes, routes)
  
if __name__ == "__main__":
  main()
