from datetime import time
from scipy.optimize import linprog 
import numpy as np
import pandas as pd
import streamlit as st


persona = ["Pedro" , "Alicia"]
posturas = ["P1", "P2", "P3"]

E0j = np.array([200, 150])  # energia inicial del participante j
Pp0j = np.array([5, 10])    # placer inicial del participante j 
Cij = np.array([[2,2,4],[3,1,3]]) 
Paij = np.array([[5,1,2],[3,8,5]])
Pj = np.array([150 , 130]) 

c = np.ones(3)
A_ub = np.concatenate((Cij, -1* Paij))
b_ub = np.concatenate((E0j,-1*Pj + Pp0j)) 
bound = (0,None)




energia = pd.DataFrame(
  Cij,
  columns= posturas,
)


placer = pd.DataFrame(
  Paij,
  columns= posturas
)


energiaInicial = pd.DataFrame (
  E0j, 
  index= persona
)

placerInicial = pd.DataFrame(
  Pp0j,
  index= persona
)

st.title('Sex App')
st.sidebar.header("Sex App")


optionsPositions = st.multiselect(
  'Selecciona las posturas', 
  ['La bicicleta' , 'Cara a Cara' , 'El Enchufe' , 'Perro tumbado' , 'Pequenna Cuchara' , 'EL puente 69' ]
)

st.subheader('Energia consumida por unidad de tiempo')
st.dataframe(energia)


st.subheader ('Placer generado por unidad de tiempo')
st.dataframe(placer)


st.subheader('Energia inicial de los participantes')
st.bar_chart(energiaInicial,use_container_width=False)

st.subheader('Placer inicail de los particiapantes')
st.bar_chart(placerInicial,use_container_width=False)



result= linprog(c = c , A_ub= A_ub, b_ub = b_ub , bounds= bound, method='simplex')
st.subheader('Tiempo dedicado a cada postura')

timeresult = pd.DataFrame(
  result.x,
  index= posturas,
)

st.line_chart(timeresult)



title = st.text_input('Movie title ' , 'Life of Brian')
st.write('The current movie title is', title) 

values = st.slider(
  'Select a range of values', 
  0.0,100.0, (25.0,75.0)
)


col1, col2 , col3 = st.columns(3)

with col1:
    with st.form('Form1'):
        st.selectbox('Select flavor', ['Vanilla', 'Chocolate'], key=1)
        st.slider(label='Select intensity', min_value=0, max_value=100, key=4)
        submitted1 = st.form_submit_button('Submit 1')

with col2:
    with st.form('Form2'):
        st.selectbox('Select Topping', ['Almonds', 'Sprinkles'], key=2)
        st.slider(label='Select Intensity', min_value=0, max_value=100, key=3)
        submitted2 = st.form_submit_button('Submit 2')

with col3:
    with st.form('Form3'):
        st.selectbox('Select Position', ['Perrito', 'Sesentaynueve'], key=2)
        st.slider(label='Select Intensity', min_value=0, max_value=100, key=3)
        submitted2 = st.form_submit_button('Submit 2')