import numpy as np
import pandas as pd
import statsmodels.api as sm

def carregar_dados(arquivo):
  df = pd.read_excel(arquivo)
  return df

def processar_dados(df):
  df['ln_Y'] = np.log(df['Yield'])
  df['ln_D'] = np.log(df['Distance'])
  return df

def realizar_regressao(df):
  X = df[['ln_D']]
  X = sm.add_constant(X)
  y = df['ln_Y']

  model = sm.OLS(y, X).fit()
  ln_Ky, alpha1 = model.params
  r2 = model.rsquared

  return ln_Ky, alpha1, r2

def processar(arquivo, descricao):
  df = carregar_dados(arquivo)
  df = processar_dados(df)
  ln_Ky, alpha1, r2 = realizar_regressao(df)

  print(descricao)
  print(f'ln(Ky): {ln_Ky}')
  print(f'alpha1: {alpha1}')
  print(f'r2: {r2}')
  print('')  

def main():
  processar('input1.xlsx', 'Resultados do Pereira (cenário 2):')
  processar('input2.xlsx', 'Todos os valores do cenário 1:')
  processar('input3.xlsx', 'Apenas Chapecó (origem ou destino) com valores do cenário 1:')

if __name__ == '__main__':
  main()
