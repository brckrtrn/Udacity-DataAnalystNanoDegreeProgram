import csv, sqlite3
import pandas as pd

#Connect to db and create new cursor
con = sqlite3.connect("OpenStreetMap.db")
con.text_factory = str
cur = con.cursor()

#Read sql script from file to Create table
fd = open("data_schema.sql", 'r')
sqlFile = fd.read()
fd.close()

#Run Create Table Script
cur.executescript(sqlFile)
con.commit()

#Insert data to SqlLite from csv
df = pd.read_csv("nodes.csv")
df.to_sql("nodes", con, if_exists='append', index=False)
con.commit()

#Insert data to SqlLite from csv
df = pd.read_csv("nodes_tags.csv")
df.to_sql("nodes_tags", con, if_exists='append', index=False)
con.commit()

#Insert data to SqlLite from csv
df = pd.read_csv("ways.csv")
df.to_sql("ways", con, if_exists='append', index=False)
con.commit()

#Insert data to SqlLite from csv
df = pd.read_csv("ways_nodes.csv")
df.to_sql("ways_nodes", con, if_exists='append', index=False)
con.commit()

#Insert data to SqlLite from csv
df = pd.read_csv("ways_tags.csv")
df.to_sql("ways_tags", con, if_exists='append', index=False)
con.commit()

con.close()
