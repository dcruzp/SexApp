import streamlit as st
import sqlite3

# Globals Varaibles
MAX_LENGTH_DESCIPTION = 400
MIN_LENGTH_DESCIPTION = 10

dblocation = "db\\sexapp.db"


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