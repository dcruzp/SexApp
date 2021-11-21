from datetime import time
from os import popen
from pprint import pprint
from urllib.parse import quote
from scipy.optimize import linprog 
import numpy as np
import pandas as pd
import streamlit as st
import sqlite3

persona = ["Pedro" , "Alicia"]
posturas = ["P1", "P2", "P3"]

E0j = np.array([200, 150])  # energia inicial del participante j
Pp0j = np.array([5, 10])    # placer inicial del participante j 
Cij = np.array([[2,2,4],[3,1,3]]) 
Paij = np.array([[5,1,2],[3,8,5]])
Pj = np.array([150 , 130]) 

c = np.ones(3)
A_ub = np.concatenate((Cij, -1* Paij))
b_ub = np.concatenate((E0j,-1*Pj + Pp0j)) 
bound = (0,None)



energia = pd.DataFrame(Cij,columns= posturas,)
placer = pd.DataFrame(Paij, columns= posturas)
energiaInicial = pd.DataFrame (E0j, index= persona)
placerInicial = pd.DataFrame(Pp0j, index= persona)


st.set_page_config(page_title='Sex App')
st.title('Sex App')
st.sidebar.header("Sex App")

dblocation = "db\\sexapp.db"

choice = st.sidebar.selectbox('Select view' ,['Main' , 'Postures'])

def get_postures_info():
  conn = sqlite3.connect(dblocation)
  cursor = conn.cursor() 
  query = cursor.execute('SELECT name,source,description FROM posturas')
  rows = query.fetchall()
  names = list(map(lambda x : x[0], rows))
  sources = list(map(lambda x : x[1], rows))
  descriptions = list(map(lambda x : x[2], rows))
  return (names, sources ,descriptions)

def show_postures():
  names, sources , descriptions =  get_postures_info()
  
  for i in range (len(names)):
    with st.expander(names[i]):
      st.write(descriptions[i])
      st.image(sources[i])

# esto es de prueba 
#obteniendo posturas de la base de datos ----------------------------------------------

def show_main_page(): 

  conn = sqlite3.connect(dblocation)
  cursor = conn.cursor()

  query = cursor.execute('SELECT name FROM posturas')
  rows = query.fetchall()
  postures = list(map(lambda x: x[0] , rows))
  cursor.close()
  conn.close()

  optionsPositions = st.multiselect('Selecciona las posturas', postures , help="Esto es una ayuda")



  st.subheader('Energia consumida por unidad de tiempo')
  st.dataframe(energia)


  st.subheader ('Placer generado por unidad de tiempo')
  st.dataframe(placer)


  st.subheader('Energia inicial de los participantes')
  st.bar_chart(energiaInicial,use_container_width=False)

  st.subheader('Placer inicail de los particiapantes')
  st.bar_chart(placerInicial,use_container_width=False)



  result= linprog(c = c , A_ub= A_ub, b_ub = b_ub , bounds= bound, method='simplex')
  st.subheader('Tiempo dedicado a cada postura')

  timeresult = pd.DataFrame(result.x,index= posturas)

  st.line_chart(timeresult)



  title = st.text_input('Movie title ' , 'Life of Brian')
  st.write('The current movie title is', title) 

# values = st.slider(
#   'Select a range of values', 
#   0.0,100.0, (25.0,75.0)
# )


# col1, col2 , col3 = st.columns(3)

# with col1:
#     with st.form('Form1'):
#         st.selectbox('Select flavor', ['Vanilla', 'Chocolate'], key=1)
#         st.slider(label='Select intensity', min_value=0, max_value=100, key=4)
#         submitted1 = st.form_submit_button('Submit 1')

# with col2:
#     with st.form('Form2'):
#         st.selectbox('Select Topping', ['Almonds', 'Sprinkles'], key=2)
#         st.slider(label='Select Intensity', min_value=0, max_value=100, key=3)
#         submitted2 = st.form_submit_button('Submit 2')

# with col3:
#     with st.form('Form3'):
#         st.selectbox('Select Position', ['Perrito', 'Sesentaynueve'], key=2)
#         st.slider(label='Select Intensity', min_value=0, max_value=100, key=3)
#         submitted2 = st.form_submit_button('Submit 2')


# with st.expander("See Explanation"):
#   st.write("esto se eirsdif ndsfnfngisdjfsrf]sdfsdsdgsfgdfghlrhthig frglhdfjg rg hjkgn srhgfhg ks")
#   st.image("https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/19870573-ead9-41ce-ba84-84acaf6569c8-1620828758.jpeg?crop=1xw:1xh;center,top&resize=480:*")

# for i in range(len(persona)):  
#   with st.expander(persona[i]):
#     for j in range (len(posturas)):
#       st.slider(label=posturas[j] , min_value=0, max_value=100, value=40 ,key=i*len(posturas)+j)


if choice == 'Main':
  show_main_page()
elif choice == 'Postures':
  show_postures()