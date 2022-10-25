import pandas
import csv
import sqlite3
conn = sqlite3.connect("db.sqlite3")
df = pandas.read_csv("final_data_v4.csv", encoding='utf-8')
print(df[0:5])
df.to_sql('course', conn, if_exists='append', index=False)
