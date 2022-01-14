from scipy.optimize import linprog 
import numpy as np
import pandas as pd
import streamlit as st
import sqlite3


#ECUT : Econsumida por unidad de tiempo [][]
#PGUT : Placer generado por unidad de Tiempo [][]
#EIP : Energía inicial del participante []
#PIP : Placer inicial de los participantes  []
#NPPOO : Placer necesario para alcanzar el orgasmo []





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



def show_main_page(): 

  conn = sqlite3.connect(dblocation)
  cursor = conn.cursor()

  query = cursor.execute('SELECT name FROM posturas')
  rows = query.fetchall()
  postures = list(map(lambda x: x[0] , rows))
  cursor.close()
  conn.close()

  optionsPositions = st.multiselect('Selecciona las posturas', postures , help="Esto es una ayuda")
  # st.write('las posturas son', optionsPositions)
  
  cant_participantes = st.number_input('Entre la cantidad de participantes',min_value=2 , max_value=15, step=1)
  participantes = [ 'P' + str(item+1) for item in range(int(cant_participantes))]
  # st.write('los participantes son' , participantes)

  
  st.subheader('Energia consumida por unidad de tiempo')
  ECUT = [[] for item in range (len(participantes))]
  for i in range(len(participantes)):
    with st.expander(participantes[i]):
      for j in range(len(optionsPositions)):
        ECUT[i].append(st.slider(optionsPositions[j],min_value=1 , max_value=40,key= 'ECUT' + str(i*len(optionsPositions) + j)))

  st.dataframe(ECUT)


  st.subheader ('Placer generado por unidad de tiempo')
  PGUT = [[]for item in range(len(participantes))]
  for i in range(len(participantes)):
    with st.expander(participantes[i]):
      for j in range(len(optionsPositions)):
        PGUT[i].append(st.slider(optionsPositions[j], min_value=1, max_value=20 ,key= 'ECUT' + str(i*len(optionsPositions) + j)))
  st.dataframe(PGUT)


  st.subheader('Energia inicial de los participantes')
  EIP = []
  with st.expander('Energia inicial de cada participante'):
    for i in range (len(participantes)):
      EIP.append(st.slider(participantes[i], min_value= 1 , max_value= 300 , key='EIP' + str(i)))
  st.bar_chart(EIP,use_container_width=False)

  st.subheader('Placer inicial de los particiapantes')
  PIP = []
  with st.expander('Placer inicial de los participantes'):
    for i in range(len(participantes)):
      PIP.append(st.slider(participantes[i], min_value=1, max_value=20 , key= 'PIP' + str(i)))
  st.bar_chart(PIP,use_container_width=False)

  st.subheader('Niveles de placer de cada participante para obtener el orgasmo')
  NPPOO = [] 
  with st.expander('Niveles de placer para obtener el orgasmo'): 
    for i in range (len(participantes)):
      NPPOO.append(st.slider(participantes[i], min_value=150 , max_value=300, key= 'NPPOO'+ str(i)))
  st.bar_chart(NPPOO,use_container_width=False)

  c = np.ones(len(optionsPositions))
  
  A_ub = np.concatenate((ECUT, -1* np.array(PGUT)))
  b_ub = np.concatenate((EIP,-1* np.array(NPPOO) +PIP))

  result= linprog(c = c , A_ub= A_ub, b_ub = b_ub , bounds= (0,None), method='simplex')
  st.subheader('Tiempo dedicado a cada postura')
  print(result)
  timeresult = pd.DataFrame(result.x , index=optionsPositions)

  st.line_chart(timeresult)



  # title = st.text_input('Movie title ' , 'Life of Brian')
  # st.write('The current movie title is', title) 

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