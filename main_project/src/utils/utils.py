import numpy as np
from utils.file_utils import routes, airplanes

def calc_yield(distance: float):
  ln_Ky = 4.711637790213505
  alpha1 = -0.7924437627341041
  return np.exp(ln_Ky + alpha1 * np.log(distance))

def calc_cask(seats: int, distance: float):
  ln_Kc = 1.7289123831498472
  beta1 = -0.3567084790912499
  beta2 = -0.4045341566648135
  return np.exp(ln_Kc + beta1 * np.log(seats) + beta2 * np.log(distance))

def calc_fare(distance: float):
  ln_Ky = 4.711637790213505
  alpha1 = -0.7924437627341041
  return np.exp(ln_Ky + alpha1 * np.log(distance)) * distance

def get_data():
  try:
    return airplanes(), routes()
  except Exception as e:
    raise Exception(f'Erro ao carregar os dados: {e}')
