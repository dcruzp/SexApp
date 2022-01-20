
import streamlit as st
import sqlite3
from addparticipants import addparticipant
import pandas as pd
import solve4

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



def show_modelo_4():

  st.title('Minimizar energia inicial de todos los participantes de forma que al terminar todos hayan alcanzado el orgasmo y tengan la misma energia')

  st.write("""
    Este problema se centra en encontrar cuanta energia
    inicial debe tener cada participante para que al analizar
    el acto sexual todos los participantes tengan la misma
    energia
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


  # st.subheader('Energía inicial de los participantes')
  # EIP = []
  # with st.expander('Energía inicial de cada participante'):
  #   for i in range (len(participants)):
  #     EIP.append(st.slider(participants[i], min_value= 1 , max_value= 300 , key='EIP' + str(i)))
  
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
  if st.button("Analizar"): 
    result = solve4.Solve4thProblem(ECUT,PGUT,NPPOO,PIP,participants,optionsPositions)

    positions_variables = [name.varValue for name in result.variables() if inlist(name.name, optionsPositions)]
    participants_variables = [name.varValue for name in result.variables() if inlist(name.name , participants)]
    
    timeresult = pd.DataFrame(positions_variables, index=optionsPositions)
    
    container = st.container()
    
    # grafica de tiempo por posiciones 
    container.markdown('#### Graficas de tiempos por posiciones')
    container.area_chart(timeresult)

    # grafica de energia inicial por participantes 
    container.markdown('#### Graficas de energia inicial por participantes')
    energiainicialresult = pd.DataFrame(participants_variables,index= participants)
    container.bar_chart(energiainicialresult)

    # grafica de energia final por participantes

    example = []
    for participant in range(len(participants)):
      sum =0 
      for posture in range(len(optionsPositions)):
        sum += positions_variables[posture] * ECUT[participant][posture]
      example.append(sum)
    print(example)


def inlist (name, optionsPositions):
  characters = '_? '
  aux_name = ''.join( x for x in name if x not in characters)

  for pos in optionsPositions:
    aux_pos = ''.join( x for x in pos if x not in characters)
    if aux_name == aux_pos:
      return True
  return False
