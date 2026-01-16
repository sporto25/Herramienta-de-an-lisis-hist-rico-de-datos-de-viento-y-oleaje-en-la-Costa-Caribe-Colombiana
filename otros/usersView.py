import sqlite3
import pandas as pd

conn = sqlite3.connect("usuarios.db")
df = pd.read_sql("SELECT * FROM usuarios", conn)
print(df)
conn.close()
