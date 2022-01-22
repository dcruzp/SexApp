import streamlit as st
import sqlite3
from addparticipants import addparticipant
import pandas as pd
import solve4
import hydralit_components as hc

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

  menu_data = [
    {'id': 'selectpositions','icon': "plus-square", 'label':"Posiciones" },
    {'id': 'selectpersons','icon':"plus-square",'label':"Personas"},
    {'id': 'ecut','icon':"plus-square",'label':"ECUT"},
    {'id': 'pgut','icon':"plus-square",'label':"PGUT"},
    # {'id': 'eip','icon':"plus-square",'label':"EIP"},
    {'id': 'pip','icon':"plus-square",'label':"PIP"},
    {'id': 'nppoo','icon':"plus-square",'label':"NPPOO"},
    {'id': 'analisis','icon':"plus-square",'label':"Analizar"},
]

  over_theme = {'txc_inactive': '#FFFFFF'}
  menu_id = hc.nav_bar(
      menu_definition=menu_data,
      override_theme=over_theme,
      home_name='Home',
      login_name='Logout',
      hide_streamlit_markers=False, #will show the st hamburger as well as the navbar now!
      sticky_nav=False, #at the top or not
      sticky_mode='pinned', #jumpy or not-jumpy, but sticky or pinned
  )


  col1 , col2 , col3 = st.columns([2,4,2])

  with col1:
    st.subheader('Minimizar energia inicial de todos los participantes de forma que al terminar todos hayan alcanzado el orgasmo y tengan la misma energia')

  with col2:

    if menu_id == 'Home':
      st.write("""
        Este problema se centra en encontrar cuanta energia
        inicial debe tener cada participante para que al finalizar
        el acto sexual todos los participantes tengan la misma
        energia
      """)
  
    if menu_id == 'selectpositions':
      st.session_state['positions'] = get_selected_postures()



    elif menu_id == 'selectpersons':
      addparticipant('participant')


    elif menu_id == 'ecut':
      st.subheader('Energía consumida por unidad de tiempo')

      participants = st.session_state['persons']
      optionsPositions = st.session_state['positions']

      ECUT = [ [1 for i in optionsPositions] for item in participants]
      # print(participants)
      # print(optionsPositions)
      print(ECUT)
      for i in range(len(participants)):
        with st.expander(participants[i]):
          for j in range(len(optionsPositions)):
            current_value = 1 
            if 'ECUT' in st.session_state:  
              try:
                current_value = st.session_state['ECUT'][i][j]
              except Exception as e:
                print('Hubo una excepcion al actualizar el valor actual de la  ECUT : ', e)
            ECUT[i][j] = st.slider(optionsPositions[j],min_value=1 , max_value=40, value = current_value,key= 'ECUT_' + str(i*len(optionsPositions) + j))
      print('se actauliza el ECUT') 
      st.session_state['ECUT'] = ECUT


    elif menu_id == 'pgut':
      st.subheader ('Placer generado por unidad de tiempo')

      participants = st.session_state['persons']
      optionsPositions = st.session_state['positions']

      PGUT = [ [1 for i in optionsPositions] for item in participants]
      for i in range(len(participants)):
        with st.expander(participants[i]):
          for j in range(len(optionsPositions)):
            print('(',i,j,')')
            current_value = 1
            if 'PGUT' in st.session_state: 
              try:
                current_value = st.session_state['PGUT'][i][j]
              except Exception as e:
                print('Hubo una excepcion al actualizar el valor actual del PGUT : ', e)
            PGUT[i][j]= st.slider(optionsPositions[j], min_value=1, max_value=20 ,value= current_value,key= 'PGUT' + str(i*len(optionsPositions) + j))
      st.session_state['PGUT'] = PGUT

    elif menu_id == 'pip':
      st.subheader('Placer inicial de los particiapantes')
      participants = st.session_state['persons']

      PIP = [1 for item in participants]
      with st.expander('Placer inicial de los participantes'):
        for i in range(len(participants)):
          current_value = 1 
          if 'PIP' in st.session_state:
            current_value = st.session_state['PIP'][i]
          PIP[i] = st.slider(participants[i], min_value=1, max_value=20 , value=current_value , key= 'PIP' + str(i))
      st.session_state['PIP'] = PIP

    elif menu_id == 'nppoo':
      st.subheader('Niveles de placer de cada participante para obtener el orgasmo')
      participants = st.session_state['persons']
      NPPOO = [1 for item in participants] 
      with st.expander('Niveles de placer para obtener el orgasmo'): 
        for i in range (len(participants)):
          current_value = 1 
          if 'NPPOO' in st.session_state:
            current_value = st.session_state['NPPOO'][i]
          NPPOO[i] = st.slider(participants[i], min_value=150 , max_value=300 ,value = current_value, key= 'NPPOO'+ str(i))
      st.session_state['NPPOO'] = NPPOO

    elif menu_id == 'analisis':
      if st.button("Hacer Analisis"):

        ECUT = st.session_state['ECUT']
        PGUT = st.session_state['PGUT']
        EIP = st.session_state['EIP']
        PIP = st.session_state['PIP']
        NPPOO = st.session_state['NPPOO']
        participants = st.session_state['persons']
        optionsPositions = st.session_state['positions']

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
