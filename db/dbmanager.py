import sqlite3
from pprint import pprint
from Scrapping.scrapping import get_posturas

conn = sqlite3.connect('sexapp.db')
c = conn.cursor() 

def create_table (): 
  c.execute("CREATE TABLE IF NOT EXISTS posturas (id INTEGER, name TEXT , source TEXT, description TEXT)")

def data_entry(tabla , data):
  for item in data:
    print(f'INSERT INTO {tabla} VALUES({item[0]},"{item[1]}","{item[2]}", "{item[3]}")')   
    c.execute(f'INSERT INTO {tabla} VALUES({item[0]},"{item[1]}","{item[2]}", "{item[3]}")')

  conn.commit()
  
def drop_table (name):
  c.execute(f'DROP TABLE "{name}"') 


# posturas = get_posturas()
# create_table()
# data_entry('posturas', posturas)

c.close()
conn.close()


