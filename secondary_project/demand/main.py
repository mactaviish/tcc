import pandas as pd

ENTRADA = '2024'

df = pd.read_excel(
  f'{ENTRADA}.xlsx',
  converters={
    'TARIFA': lambda x: float(str(x))
  }
)

resultado = (
  df
    .groupby(['ORIGEM', 'DESTINO'], as_index=False)
    .agg(
      tarifa   = ('TARIFA', 'mean'),
      assentos = ('ASSENTOS', 'sum')
    )
)

resultado.columns = ['origin', 'destination', 'demand', 'fare']

resultado.to_excel(f'{ENTRADA}_GROUPED.xlsx', index=False)
