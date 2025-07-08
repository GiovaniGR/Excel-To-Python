import pandas as pd
import mysql.connector

def mudanca_valores(df, colunas):
    for col in colunas:
      df[col] = df[col].astype(str).str.replace('.', '', regex=False).str.replace(',','.',regex=False)
      df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)
      return df

df = pd.read_excel("dados/Financeiro.xlsx", skiprows=1)

colunas_double=('ENTRADA', 'SAIDA')
df = mudanca_valores(df, colunas_double)

conexaoBanco = mysql.connector.connect(
  host = 'localhost',
  user = 'root',
  password = 'giovani13',
  database = 'pymod1'
)

cursor = conexaoBanco.cursor()
sql = 'INSERT INTO PY_MOD1(DATA, CLIENTE, DOCUMENTO, ENTRADA, SAIDA)' \
  'VALUES(%s,%s,%s,%s,%s)'

for inserir, row in df.iterrows():

  valInserir = tuple (
    None if pd.isna(row[col]) else row[col]
    for col in ['DATA', 'CLIENTE', 'DOCUMENTO', 'ENTRADA', 'SAIDA']
)
  cursor.execute(sql, valInserir)

conexaoBanco.commit()
cursor.close()
conexaoBanco.close()

