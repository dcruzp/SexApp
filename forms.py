import streamlit as st 
import sqlite3



# Globals Varaibles

MAX_LENGTH_DESCIPTION = 400
MIN_LENGTH_DESCIPTION = 10


dblocation = "db\\sexapp.db"

if 'persons' not in st.session_state:
  st.session_state['persons'] = []

def deleteperson(person):
  print('trying to delete the person  ' + person)
  if person in st.session_state['persons']:
    st.session_state['persons'].remove(person)



def annadirparticipantes(key= None):
  col1, col2 = st.columns([4,2])

  with col1:

    col1.form =  st.form(key= 'form'+ str(key))
    col1.form.write("Entre los datos para un nuevo participante en el acto sexual")
      
    name = col1.form.text_input('Entra el nombre del participante:', 'nombre')

    submitted = col1.form.form_submit_button("Aceptar")
    if submitted:
      if name == '':
        col1.form.warning('El nombre no puede ser un string vacio')
      elif name.lower() in st.session_state['persons']:
        col1.form.warning("Ya existe una persona con ese nombre")
      else:
        st.session_state['persons'].append(name.lower())

  with col2:

    indexbotton = 1
    container = col2.container()
    references = [] 
    for p in st.session_state['persons']:
      container.caption(p) 
      btn = container.button('Borrar',
                             key= 'button' + str(indexbotton), 
                             on_click=deleteperson,
                             args = [p])
      indexbotton += 1
      references.append((btn,p)) 

def annadirpostura():
  form = st.form(key= 'form2')

  form.write('Entre los datos para insertar la nueva postura a la aplicacion')

  warning_name_posture = form.empty()
  posture_name = form.text_input('Entrar el nombre de la postura', 'Postura')
  
  warning_desciption_posture = form.empty()
  posture_description = form.text_input('Escriba una descripcion para la postura')
  
  warning_image_posture = form.empty()
  uploaded_file = form.file_uploader('Escoge una figura para la postura')

  try: 
    if uploaded_file is not None:
      byte_data = uploaded_file.read()
      form.image(byte_data)
  except Exception:
    warning_image_posture.warning("hobo problemas al cargar la imagen")

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
    else:
      pass 



choice = st.sidebar.selectbox('Select view' ,['Entrar las pesonas', 'Entrar una nueva postura', 'datos'])

if choice == 'Entrar las pesonas':
  annadirparticipantes(0)
  # st.write('entre las posturas')
elif choice == 'datos':
  st.write('datos')
elif choice == 'Entrar una nueva postura':
  annadirpostura()

print(st.session_state['persons'])


columns = st.columns([4,1])


# nextbutton = columns[1].button('Next')
# if nextbutton:
#   annadirparticipantes()

# st.write(st.session_state)











