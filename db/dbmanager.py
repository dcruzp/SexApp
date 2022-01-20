import sqlite3
from pprint import pprint

dblocation = "db\\sexapp.db"

def create_table (conn):
  c = conn.cursor()
  c.execute("CREATE TABLE IF NOT EXISTS posturas (id INTEGER, name TEXT , source TEXT, description TEXT)")

# def data_entry(tabla , data):
#   for item in data:
#     print(f'INSERT INTO {tabla} VALUES({item[0]},"{item[1]}","{item[2]}", "{item[3]}")')   
#     c.execute(f'INSERT INTO {tabla} VALUES({item[0]},"{item[1]}","{item[2]}", "{item[3]}")')
  # conn.commit()
  
def drop_table (name, conn):
  c = conn.cursor()
  c.execute(f'DROP TABLE "{name}"') 

def getpostures():
  conn = sqlite3.connect(dblocation)
  c = conn.cursor() 
  c.execute("SELECT name,source FROM posturas")
  rows = c.fetchall()
  postures = list(map(lambda x: x[1] , rows))
  c.close()
  conn.close()
  return postures


if __name__ == '__main__':
  
  posturas = getpostures()

  pprint (posturas)
