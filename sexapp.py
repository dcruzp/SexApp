from pygame import image
from scipy.optimize import linprog 
import numpy as np
import pandas as pd
import streamlit as st
import sqlite3
import random
import json


# Globals Varaibles
dblocation = None
MAX_LENGTH_DESCIPTION = 400
MIN_LENGTH_DESCIPTION = 10



def loadingconfigfile():
  global dblocation
  try:
    file = open ('config.json', 'r')
    config = json.load(file)
    dblocation = config['DEFAULT']['DB_DIR']
  except Exception as err:
    print ('Error reading configuration file')

loadingconfigfile()




# configurando las parametros de la pagina 
st.set_page_config( page_title='Sex App',
                    layout='centered',
                    page_icon= 'img\sex_icon.png',
                  )


# dandole un titulo a la Pagina 
st.title('Sex App')


st.sidebar.header("Sex App")

dblocation = "db\\sexapp.db"

choice = st.sidebar.selectbox('Select view' ,['Modelo 1', 'Modelo 2' , 'Modelo 3' , 'Modelo 4' , 'Modelo 5' , 'Mostrar Posturas', 'Adicionar una postura'])

choicemodel1 = st.sidebar.selectbox('Select view', ['sdfsdf', 'afsdf'])


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

def get_number_of_participants():
  number_participants = st.number_input('Entre la cantidad de participantes',min_value=2 , max_value=15, step=1)
  participants = [ 'P' + str(item+1) for item in range(int(number_participants))]
  return participants

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
  # st.write('las posturas son', optionsPositions)
  
  cant_participantes = st.number_input('Entre la cantidad de participantes',min_value=2 , max_value=15, step=1)
  participants = [ 'P' + str(item+1) for item in range(int(cant_participantes))]
  # st.write('los participantes son' , participantes)

  
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
    result = solve_model1(optionsPositions,ECUT,PGUT,EIP,NPPOO,PIP)
    timeresult = pd.DataFrame(result.x , index=optionsPositions)
    container = st.container()
    container.line_chart(timeresult)
    container.area_chart(timeresult)

def solve_model1(optionsPositions , ECUT , PGUT, EIP, NPPOO, PIP):
  c = np.ones(len(optionsPositions))
  
  A_ub = np.concatenate((ECUT, -1* np.array(PGUT)))
  b_ub = np.concatenate((EIP,-1* np.array(NPPOO) +PIP))

  result= linprog(c = c , A_ub= A_ub, b_ub = b_ub , bounds= (0,None), method='simplex')
  st.subheader('Tiempo dedicado a cada postura')
  # print(result)
  return result

@st.cache
def get_postures_info():
  conn = sqlite3.connect(dblocation)
  cursor = conn.cursor() 
  query = cursor.execute('SELECT name,source,description , image FROM posturas')
  rows = query.fetchall()
  names = list(map(lambda x : x[0], rows))
  sources = list(map(lambda x : x[1], rows))
  descriptions = list(map(lambda x : x[2], rows))
  images = list(map(lambda x : x[3], rows))
  return (names, sources ,descriptions,images)

def show_all_postures():
  names, sources , descriptions ,images =  get_postures_info()
  for i in range (len(names)):
    with st.expander(names[i]):
      st.write(descriptions[i])
      if sources[i] is not None:
        st.image(sources[i])
      elif images[i] is not None:
        st.image(images[i])

def addposture():
  form = st.form(key= 'form2')

  form.write('Entre los datos para insertar la nueva postura a la aplicacion')

  warning_name_posture = form.empty()
  posture_name = form.text_input('Entrar el nombre de la postura', 'Postura')
  
  warning_desciption_posture = form.empty()
  posture_description = form.text_input('Escriba una descripcion para la postura', "Descripcion para la postura ")
  
  warning_image_posture = form.empty()
  uploaded_file = form.file_uploader('Escoge una figura para la postura')

  submitted = form.form_submit_button("Aceptar")

  if submitted:
    if (len(posture_name) > 50) or posture_name == '':
      warning_name_posture.warning('el nombre de la postura no puede ser vacio ni exceder los 50 caracteres')
    elif (
      (len(posture_description) < MIN_LENGTH_DESCIPTION) 
        or 
      (len(posture_description) > MAX_LENGTH_DESCIPTION) 
      ):
      warning_desciption_posture.warning('la descripcion de la postura debe tener una longitud entre 100 y 400')
    elif uploaded_file is None:
      warning_image_posture.warning('no se ha seleccionado ninguna imagen para  la postura')
    else:
      try: 
        byte_data = uploaded_file.read()

        buff = sqlite3.Binary(byte_data)


        conn = sqlite3.connect(dblocation)
        c = conn.cursor()
        
        c.execute(f'INSERT INTO posturas (name, description , image)  VALUES ("{posture_name}" , "{posture_description}", ?);', (buff,))
        conn.commit()
        c.close()
        conn.close()

        form.success('La postura ha sido annadida exitosamente')
      except Exception as err:
        warning_image_posture.warning('Hubo un error al insertar en la base de datos %s' % err)


if choice == 'Modelo 1':
  show_modelo_1()
elif choice == 'Mostrar Posturas':
  show_all_postures()
elif choice == 'Adicionar una postura':
  addposture()
