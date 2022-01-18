from scipy.optimize import linprog 
import numpy as np
import pandas as pd
import streamlit as st
import sqlite3
import os
from sexapp import *
import solve2

#ECUT : E consumida por unidad de tiempo [][]
#PGUT : Placer generado por unidad de Tiempo [][]
#EIP : Energía inicial del participante []
#PIP : Placer inicial de los participantes  []
#NPPOO : Placer necesario para alcanzar el orgasmo []



def show_second_page(): 
  file_path = os.path.realpath(__file__)
  dblocation = file_path.append("db\\sexapp.db") 
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
  participantes = [ 'Participante #' + str(item+1) for item in range(int(cant_participantes))]
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

  result= solve2.Solve2ndProblem(ECUT,PGUT,EIP,PIP,NPPOO,participantes,optionsPositions)
  result.sol
  st.subheader('Tiempo dedicado a cada postura')
  print(result)
  timeresult = pd.DataFrame(result.values() , index=optionsPositions)

  st.line_chart(timeresult)

