import streamlit as st
import sqlite3
from addparticipants import addparticipant
import numpy as np
import pandas as pd
from scipy.optimize import linprog
import solve5
import hydralit_components as hc

dblocation = "db\\sexapp.db"


def get_selected_postures():
    conn = sqlite3.connect(dblocation)
    cursor = conn.cursor()

    query = cursor.execute('SELECT name FROM posturas')
    rows = query.fetchall()
    postures = list(map(lambda x: x[0], rows))
    cursor.close()
    conn.close()
    options_positions = st.multiselect('Selecciona las posturas', postures,
    default=postures[0], help="Seleccione las posturas que desea realizar en el acto sexual")
    return options_positions


def show_modelo_5():
  menu_data = [
    {'id': 'selectpositions','icon': "plus-square", 'label':"Posiciones" },
    {'id': 'selectpersons','icon':"plus-square",'label':"Personas"},
    {'id': 'ecut','icon':"plus-square",'label':"ECUT"},
    {'id': 'pgut','icon':"plus-square",'label':"PGUT"},
    {'id': 'eip','icon':"plus-square",'label':"EIP"},
    {'id': 'personamarginal','icon':"plus-square",'label':"Persona Marginal"},
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
    st.title(
        'Maximizar el placer inicial de un participante específico.')


  with col2:
    
    if menu_id == 'Home':
      st.write("""
      En este modelo se intenta maximizar el placer inicial de un
      participante específico, de forma tal que
      todos los participantes, excepto el
      específico, alcancen el orgasmo. Para ello se utiliza una restricción extra sobre la persona que no
      debe alcanzar un orgasmo, y se maximiza una variable arbitraria h, que representa el placer inicial de dicha persona.
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
    # st.bar_chart(EIP,use_container_width=False)

    elif menu_id == 'eip':
      st.subheader('Energía inicial de los participantes')
      participants = st.session_state['persons']
      EIP = [1 for item in participants]
      with st.expander('Energía inicial de cada participante'):
        for i in range (len(participants)):
          current_value = 1 
          if 'EIP' in st.session_state:
            current_value = st.session_state['EIP'][i]
          EIP[i] = st.slider(participants[i], min_value= 1 , max_value= 300 ,value=current_value, key='EIP' + str(i))
      st.session_state['EIP'] = EIP

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

    elif menu_id == 'personamarginal':

      participants = st.session_state['persons']

      choice = st.selectbox(
        'Selecciona la persona a marginar', participants, key='personsSideabar')
      personIndex = 0

      if 'pm' not in st.session_state:
        st.session_state['pm'] = personIndex
      
      for i in range(len(participants)):
          if choice == participants[i]:
              personIndex = i
      st.session_state['pm'] = personIndex
      



    
    elif menu_id == 'analisis':
      if st.button("Hacer Analisis"):

        ECUT = st.session_state['ECUT']
        PGUT = st.session_state['PGUT']
        EIP = st.session_state['EIP']
        PIP = st.session_state['PIP']
        NPPOO = st.session_state['NPPOO']
        participants = st.session_state['persons']
        optionsPositions = st.session_state['positions']
        personIndex = st.session_state['pm']



        result = solve5.Solve5thProblem(
            ECUT, PGUT, EIP, PIP, NPPOO, participants, optionsPositions, personIndex)

        sol = []
        for name in result.variables():
            if name.name == "H":
                continue

            sol.append(name.varValue)

        if result.status == 1:
            timeresult = pd.DataFrame(sol, index=optionsPositions)
            container = st.container()
            container.line_chart(timeresult)
            container.area_chart(timeresult)

            #Guaradando los placeres de todos en una lista de placeres [ persona[placer]]
            pleasureForEverybody = []
            for personIndex in range(len(participants)):
                temp1 = []
                for postureIndex in  range(len(optionsPositions)):
                    temp1.append(sol[postureIndex] * PGUT[personIndex][postureIndex])

                pleasureForEverybody.append(temp1)

                st.subheader('Gráfico de Placer por posición de '+participants[personIndex])
                data = pd.DataFrame({
                'index': optionsPositions,
                'Placer por posición': pleasureForEverybody[personIndex],
                }).set_index('index')
                st.bar_chart(data)

            #Guardando las energías de todos en una lista de energías [ persona[energía]]
            energyForEverybody = []
            for personIndex in range(len(participants)):
                temp1 = []
                for postureIndex in  range(len(optionsPositions)):
                    temp1.append(sol[postureIndex] * ECUT[personIndex][postureIndex])


                energyForEverybody.append(temp1)

                st.subheader('Gráfico de enrgía consumida por posición de '+participants[personIndex])
                data = pd.DataFrame({
                'index': optionsPositions,
                'Energía por posición': energyForEverybody[personIndex],
                }).set_index('index')
                st.bar_chart(data)



        elif result.status == 0:
            st.title('No se resolvió el problema.')

        elif result.status == -1:
            st.title('El problema es inviable.')

        elif result.status == -2:
            st.title('El problema es ilimitado.')

        elif result.status == -3:
            st.title('El problema es indefinido')

    