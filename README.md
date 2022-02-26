# ¿Existe un acto sexual Ideal?

## Abstract

Si se tiene un conjunto prefijado de posturas sexuales que se quieren usar en un acto sexual en un orden predeterminado, es posible construir un modelo de programación lineal donde las variables indican cuánto tiempo dedicarle a cada postura, de forma que se cumplan algunas restricciones de sentido común y se maximice (o minimice) algún criterio. El criterio que se debe maximizar (o minimizar) depende de cada situación y de cada usuario. Algunos ejemplos pueden ser maximizar el placer, o minimizar el cansancio logrando determinados niveles de placer.

### Objetivos

Los objetivos de este trabajo son varios:

1. Se desea tener una aplicación en la que el usuario pueda entrar determinados datos de placer y agotamiento que proporciona cada postura, seleccionar qué criterio se quiere maximizar o minimizar y qué restricciones tener en cuenta, y obtener los resultados del modelo. Aquí se deberían graficar las curvas de placer y agotamiento para los datos entrados.
2. Se desean construir en interpretar los problemas duales de los planteados en el trabajo del año 2016, para poder brindarle al usuario información sobre las variables duales en el óptimo.
3. Extender el trabajo. Aquí se asume que las posturas y el orden están fijas. Se desea construir (y resolver) un modelo en el que el orden de las posiciones sea parte de lo que hay que decidir.



#### Datos

#### Restricciones comunes

1. Después de cada postura, la energía de cada participante disminuye de manera proporcional al tiempo que se permanezca en ella: 
   $$
   A_{ij} = A_{(i-1)j} - C_{ij} X_i  \hspace{1cm} \forall i \in N \hspace{1cm} \forall j \in J
   $$

2. Después de cada postura el placer de cada participante aumenta de manera proporcional al tiempo que permanezca en ella: 
   $$
   P_{ij} = P_{(i-1)j} + Pa_{ij} X_i  \hspace{1cm} \forall i \in N \hspace{1cm} \forall j \in J
   $$

3. En todo momento la energía es mayor o igual que cero: 
   $$
   A{ij} \geq 0  \hspace{1cm} \forall i \in N \hspace{1cm} \forall j \in J
   $$

4. El placer  después del acto sexual es mayor o igual que al placer necesario para alcanzar al orgasmo. 
   $$
   P_{nj}  \geq \hat{P}_{j}  \hspace{1cm} \forall j \in J   
   $$
   

### Maximizar la duración del acto sexual 

Este problema se centra en encontrar que tiempo se debe estar en cada posición para que el tiempo del acto sexual sea el mayor posible. Se utiliza $x_i$ que indica el tiempo que se permanecerá en cada postura y se resuelva el problema  que se presenta a continuación , sujeta a las restricciones que se 1,2,3,4.
$$
max \sum_{i=1}^{n} x_i
$$


### Como correr la aplicación 

Para correr la aplicación por primera vez es necesario instalar primero todas las dependencias, para esto se puede correr el siguiente comando en la lista de comandos 
```
pip install -r requirements.txt
``` 

En el fichero ```requeriments.txt``` están todas las librerías con los paquetes necesarios y la especificación de cada version de los paquetes que hay que instalar para que la aplicación funcione correctamente. Los paquetes que hay en el fichero ```requeriments.txt``` se muestran a continuación: 

```
beautifulsoup4==4.10.0
hydralit_components==1.0.9
numpy==1.22.1
pandas==1.3.5
PuLP==2.6.0
scipy==1.7.3
streamlit==1.4.0
streamlit_option_menu==0.2.10
```

## Para correr la aplicación 

En la raíz del proyecto hay uh fichero llamado ```sexapp.py``` que es donde esta el main principal del proyecto, es decir donde se encuentra la entrada de la aplicación de **streamlit**. Para correr  la aplicación hay abrir una terminal justo en donde se encuentra la raíz de la aplicación, y entonces se corre el siguiente comando: 

```  
streamlit run sexapp.py
```


### Authors
- [Daniel de la cruz Prieto](http://github.com/dcruzp/)
- [Dayron Fernandez Acosta](https://github.com/I-Dayz-I)
- [Javier Villar Alonso](https://github.com/Vyler-Lnidas)
- [Julio Jose Horta](https://github.com/Belzico)
