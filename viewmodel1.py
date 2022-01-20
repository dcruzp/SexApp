import streamlit as st
import sqlite3
from addparticipants import addparticipant
import numpy as np
import pandas as pd
from scipy.optimize import linprog 
import solvepulp

dblocation = "db\\sexapp.db"


def get_selected_postures ():
  conn = sqlite3.connect(dblocation)
  cursor = conn.cursor()

  query = cursor.execute('SELECT name FROM posturas')
  rows = query.fetchall()
  postures = list(map(lambda x: x[0] , rows))
  cursor.close()
  conn.close()
  options_positions = st.multiselect('Selecciona las posturas', postures , default=postures[0], help="Seleccione las posturas que desea realizar en el acto sexual")
  return options_positions



def show_modelo_1():

  st.title('Maximizar la duración del  acto sexual')

  st.write("""
  Este problema se centra en encontrar que tiempo se debe estar en cada
  postura  para que el tiempo del acto sexual sea el mayor posible. Se 
  debe proporcionar informacion de las posturas que se van a hacer durante 
  el acto sexual. Ademas se tiene que proporcionar nformacion de los participantes 
  saber la energia inicial que estos participantes tienen , y el placer inicial de estos 
  como nombre para poder identificarlos en la aplicación. Tambien es necesario 
  junto con el placer que estos necesitan para obtener el orgasmo. Ademas la aplcacion tiene 
  que saber que placer genera y la energia que consume a cada participante cada una de las posturas
  que se desea realizar en el acto sexual. 
  """)
  
  optionsPositions = get_selected_postures()

  addparticipant()

  participants = st.session_state['persons']
  
  st.subheader('Energía consumida por unidad de tiempo')
  ECUT = [[] for item in range (len(participants))]
  for i in range(len(participants)):
    with st.expander(participants[i]):
      for j in range(len(optionsPositions)):
        ECUT[i].append(st.slider(optionsPositions[j],min_value=1 , max_value=40,key= 'ECUT' + str(i*len(optionsPositions) + j)))

  # st.dataframe(ECUT)


  st.subheader ('Placer generado por unidad de tiempo')
  PGUT = [[]for item in range(len(participants))]
  for i in range(len(participants)):
    with st.expander(participants[i]):
      for j in range(len(optionsPositions)):
        PGUT[i].append(st.slider(optionsPositions[j], min_value=1, max_value=20 ,key= 'ECUT' + str(i*len(optionsPositions) + j)))
  
  # st.dataframe(PGUT)


  st.subheader('Energía inicial de los participantes')
  EIP = []
  with st.expander('Energía inicial de cada participante'):
    for i in range (len(participants)):
      EIP.append(st.slider(participants[i], min_value= 1 , max_value= 300 , key='EIP' + str(i)))
  
  #st.bar_chart(EIP,use_container_width=False)

  st.subheader('Placer inicial de los particiapantes')
  PIP = []
  with st.expander('Placer inicial de los participantes'):
    for i in range(len(participants)):
      PIP.append(st.slider(participants[i], min_value=1, max_value=20 , key= 'PIP' + str(i)))
  
  # st.bar_chart(PIP,use_container_width=False)

  st.subheader('Niveles de placer de cada participante para obtener el orgasmo')
  NPPOO = [] 
  with st.expander('Niveles de placer para obtener el orgasmo'): 
    for i in range (len(participants)):
      NPPOO.append(st.slider(participants[i], min_value=150 , max_value=300, key= 'NPPOO'+ str(i)))
  
  # st.bar_chart(NPPOO,use_container_width=False)

  st.empty()
  if st.button("Analyce"):
    result = solvepulp.Solve1stProblem(ECUT,PGUT,EIP,PIP,NPPOO,participants,optionsPositions)
    sol= []
    for name in result.variables():
        sol.append(name.varValue)
    
    if result.status == 1:
      timeresult = pd.DataFrame(sol , index=optionsPositions)
      container = st.container()
      container.line_chart(timeresult)
      container.area_chart(timeresult)
      
    elif result.status == 0:
      st.title('No se resolvió el problema.')
    
    elif result.status == -1:
      st.title('El problema es inviable.')
    
    elif result.status == -2:
      st.title('El problema es ilimitado.')
    
    elif result.status == -3:
      st.title('El problema es indefinido')

# def solve_model1(optionsPositions , ECUT , PGUT, EIP, NPPOO, PIP):
#   c = np.ones(len(optionsPositions))
  
#   A_ub = np.concatenate((ECUT, -1* np.array(PGUT)))
#   b_ub = np.concatenate((EIP,-1* np.array(NPPOO) +PIP))

#   result= linprog(c = c , A_ub= A_ub, b_ub = b_ub , bounds= (0,None), method='simplex')
#   st.subheader('Tiempo dedicado a cada postura')
#   return result