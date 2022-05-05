El proyecto consiste en la obtención de reacciones químicas inorgánicas a partir de elementos químicos y las valencias de estos; el programa toma la información de entrada y mediante un cálculo de probabilidades, realizado con técnicas básicas de inteligencia artificial supervisada, es capaz de regresar al usuario la reacción resultante, así como una descripción general de la clasificación de dicho compuesto.
En la elaboración del presente proyecto se emplearon diversos recursos, tales como las librerías: tensorflow, nltk, tflearn, numpy, pandas, json, y streamlit.

Primera etapa: Principalmente las primeras 3 librerías mencionadas, conformaron la parte lógica de la inteligencia artificial capaz de clasificar los elementos determinados por el usuario, posteriormente entran en un proceso que arroja la probabilidad de pertenecer a un grupo en específico, establecidos previamente en un archivo Json.

Segunda etapa: Por otro lado, numpy, pandas y json permitieron procesar los resultados arrojados por la primera etapa para poder conseguir los símbolos quimicos de los elementos solicitados y acomodarlos de acuerdo a los parámetros establecidos, de modo que arrojaran el formato adecuado de la reacción química deseada.

Tercera Etapa: Finalmente, con apoyo a la librería y plataforma de host de streamlit y a las funciones provistas por la misma plataforma, se logró formalizar el front end de la página web. En este apartado, el usuario es capaz de establecer los elementos a reaccionar y posteriormente se despliega la reacción química resultante; en la parte inferior de este resultado se muestra una descripción acerca de las características físicas y químicas de la familia del producto, así como una tabla de valencias de apoyo y apartados de información adicional acerca de las reacciones químicas

MIEMBROS DEL EQUIPO:

RODRÍGUEZ RIVAS SERGIO ADRIÁN.

ROSALES SERRANO ROBERTO.

RAMÍREZ LOYA HUGO DANIEL.

RODRÍGUEZ ROA DIEGO.


