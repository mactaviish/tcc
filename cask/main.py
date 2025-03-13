import numpy as np
import pandas as pd
import statsmodels.api as sm

def carregar_dados(arquivo):
  df = pd.read_excel(arquivo)
  return df

def processar_dados(df):
  df_melted = df.melt(id_vars=['Aircraft', 'Seats'], var_name='Distance', value_name='CASK')
  df_melted['Distance'] = df_melted['Distance'].astype(float)

  df_melted['ln_C'] = np.log(df_melted['CASK'])
  df_melted['ln_S'] = np.log(df_melted['Seats'])
  df_melted['ln_D'] = np.log(df_melted['Distance'])

  return df_melted

def realizar_regressao(df_melted):
  X = df_melted[['ln_S', 'ln_D']]
  X = sm.add_constant(X)
  y = df_melted['ln_C']

  model = sm.OLS(y, X).fit()
  ln_Kc, beta1, beta2 = model.params
  r2 = model.rsquared

  return ln_Kc, beta1, beta2, r2

def calcular_cask(S, D, ln_Kc, beta1, beta2):
  return np.exp(ln_Kc + beta1 * np.log(S) + beta2 * np.log(D))

def main():
  arquivo = 'input.xlsx'
  df = carregar_dados(arquivo)
  df_melted = processar_dados(df)
  ln_Kc, beta1, beta2, r2 = realizar_regressao(df_melted)

  print(f'ln(Kc): {ln_Kc}')
  print(f'beta1: {beta1}')
  print(f'beta2: {beta2}')
  print(f'r2: {r2}')

if __name__ == '__main__':
  main()
