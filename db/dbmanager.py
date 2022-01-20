import sqlite3
from pprint import pprint

dblocation = "db\\sexapp.db"

def create_table (conn):
  c = conn.cursor()
  c.execute("CREATE TABLE IF NOT EXISTS posturas (id INTEGER, name TEXT , source TEXT, description TEXT)")

def data_entry(tabla , data):
  conn = sqlite3.connect(dblocation)
  c = conn.cursor()
  for item in data:
    print(f'INSERT INTO {tabla} (name , source, description) VALUES("{item[0]}","{item[1]}","{item[2]}")')   
    c.execute(f'INSERT INTO {tabla} (name , source, description)  VALUES("{item[0]}","{item[1]}","{item[2]}")')
  conn.commit()
  c.close()
  conn.close()
  
def drop_table (name, conn):
  c = conn.cursor()
  c.execute(f'DROP TABLE "{name}"') 

def getpostures():
  conn = sqlite3.connect(dblocation)
  c = conn.cursor() 
  c.execute("SELECT name,source FROM posturas")
  rows = c.fetchall()
  postures = list(map(lambda x: x[0] , rows))
  c.close()
  conn.close()
  return postures


if __name__ == '__main__':
  
  

  # data = [['postura1' , 
  #          'https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/19870573-ead9-41ce-ba84-84acaf6569c8-1620828758.jpeg?crop=1xw:1xh;center,top&resize=480:*', 
  #          'Descripcion de la postura 1']]

  # tabla = 'posturas'

  # data_entry(tabla, data)


  # posturas = getpostures()
  # pprint (posturas)
  pass 
