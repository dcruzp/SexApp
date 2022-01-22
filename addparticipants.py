import streamlit as st

def deleteperson(person):
  print('trying to delete the person  ' + person)
  if person in st.session_state['persons']:
    st.session_state['persons'].remove(person)


def addparticipant(key= None):

  form =  st.form(key= 'form'+ str(key))
  form.write("Entre los datos para un nuevo participante en el acto sexual")
      
  name = form.text_input('Entra el nombre del participante:', 'nombre')

  submitted = form.form_submit_button("Aceptar")
  if submitted:
    if name == '':
      form.warning('El nombre no puede ser un string vacio')
    elif name.lower() in st.session_state['persons']:
      form.warning("Ya existe una persona con ese nombre")
    else:
      st.session_state['persons'].append(name.lower())



  indexbotton = 1
  container = st.container()
  references = [] 
  for p in st.session_state['persons']:
    container.caption(p) 
    btn = container.button( 'Borrar',
                            key= 'button' + str(indexbotton), 
                            on_click=deleteperson,
                            args = [p])
    indexbotton += 1
    references.append((btn,p)) 