import streamlit as st
import nltk 
from nltk.stem.lancaster import LancasterStemmer 
stemmer = LancasterStemmer()
import tflearn 
import numpy
import tensorflow 
import json
import random
import pickle
import time
import openpyxl
import pandas as pd


datosexc=pd.read_excel('listaelem.xlsx')
df=pd.DataFrame(datosexc)

datosexc2=pd.read_excel('prefijos.xlsx')
df2=pd.DataFrame(datosexc2)
    
nltk.download('punkt')

with open("contenido.json", encoding='utf-8') as archivo: 
    datos =  json.load(archivo)  

try:
    with open("variables.pickle", "rb") as archivopickle:
        palabras, tags, entrenamiento, salida = pickle.load(archivopickle)
except:
    palabras=[]
    tags= []
    auxX=[]
    auxY=[]

    for contenido in datos["contenido"]:
        for patrones in contenido["patrones"]:
            auxpalabra = nltk.word_tokenize(patrones)
            palabras.extend(auxpalabra)
            auxX.append(auxpalabra)
            auxY.append(contenido["tag"])

            if contenido["tag"] not in tags:
                tags.append(contenido["tag"])

    palabras =[stemmer.stem(w.lower()) for w in palabras if w!="?"]
    palabras = sorted(list(set(palabras)))
    tags= sorted(tags)

    entrenamiento = []
    salida =[]

    salidavacia = [0 for _ in range(len(tags))]

    for x, documento in enumerate(auxX): 
        cubeta = []
        auxpalabra= [stemmer.stem(w.lower())for w in documento]
        for w in palabras:
            if w in auxpalabra:
                cubeta.append(1)
            else:
                cubeta.append(0)
        filasalida= salidavacia[:]
        filasalida [tags.index(auxY[x])]= 1
        entrenamiento.append(cubeta)
        salida.append(filasalida)

    entrenamiento = numpy.array(entrenamiento)
    salida = numpy.array(salida)
    with open("variables.pickle","wb") as archivopickle:
        pickle.dump((palabras, tags, entrenamiento, salida),archivopickle)

#Entra la libreria Tf para el machine learning
tensorflow.compat.v1.reset_default_graph()

red = tflearn.input_data(shape=[None, len(entrenamiento[0])])
red = tflearn.fully_connected(red, 100)
red= tflearn.fully_connected(red, 100)
red= tflearn.fully_connected(red, len(salida[0]), activation="softmax")
red = tflearn.regression(red)

modelo = tflearn.DNN(red)
try: 
    modelo.load("modelo.tflearn")
except:
    modelo.fit(entrenamiento, salida, n_epoch=1000, batch_size=50, show_metric=True)
    modelo.save("modelo.tflearn")

#Apartado de pagina web.
st.set_page_config(layout="wide")
mt1, header, mt2 = st.columns([5,5,3])
       
        
st.markdown("""
            <style>
            .big-font {
                font-size:30px !important;
            }
            </style>
            """, unsafe_allow_html=True)

with mt1:
    st.text("")

with header:
    st.image("logo.jpg", width = 300)    
    
with mt2:
    st.text("")    
    
mt6, titlep, mt7 = st.columns([4,5,3])
with mt6:
    st.text("")
    
with titlep:
    st.markdown(f'<p class="big-font">Obtencion de Reacciones Quimicas</p>', unsafe_allow_html=True)
    
with mt7:
    st.text("")   

#Funcion principal del bot
def mainbot():
    try:
        while True:  
            cols= st.columns([1,1,1,1,1,1,1,4]) 

            elemento=cols[0].selectbox("Ingrese el elemento: ", ("Elemento 1","aluminio", "bario", "berilio", "bismuto", "cadmio","calcio", "cerio", "cromo", "cobalto", "cobre", "oro",
                    "iridio", "hierro", "plomo", "litio", "magnesio", "manganeso", "mercurio", "molibdeno", "n??quel", "osmio", "paladio",
                    "platino", "potasio", "radio", "rodio", "plata", "sodio", "tantalio", "talio", "torio", "esta??o", "titanio", "volframio",
                    "uranio", "vanadio","zinc","escandio","titanio","vanadio","cromo","manganeso","hierro","cobalto","niquel","cobre","zinc",
                    "itrio","circonio","niobio","molibdeno","tecnecio","rutenio","rodio","paladio","plata","cadmio","lantano","hafnio","tantalio",
                    "tungsteno","renio","osmio","iridio","platino","oro","mercurio","actinio","rutherfordio","dubnium","seaborgio","bohrium",
                    "hassium","meitnerio","darmstadtium","roentgenio","copernico","cerio","praseodimio","neodimio","prometeo","samario",
                    "europio","gadolinio","terbio","disprosio","holmio","erbio","tulio","iterbio","lutecio","torio","protactinio","uranio",
                    "neptunio","plutonio","americio","curio","berkelio","californio","einstenio","fermio","mendelevio","nobelio","lawrencium",
                    "carbon","nitrogeno","fosforo","azufre","selenio","fluor","cloro","bromo","yodo","astato","tennessine"), key = "optelement1")
            prefijo1=int(cols[1].selectbox("Valencia 1", (-3,-2,-1,1,2,3,4,5,6,7,8,9), key= "_prefijo1"))
            cubeta= [0 for _ in range(len(palabras))]
            entradaprocesada= nltk.word_tokenize(elemento)
            entradaprocesada =[stemmer.stem(palabra.lower()) for palabra in entradaprocesada]
            for palabraindividual in entradaprocesada:
                for i, palabra in enumerate(palabras):
                    if palabra == palabraindividual:
                        cubeta[i] = 1
            resultados = modelo.predict([numpy.array(cubeta)])
            resultadosindices= numpy.argmax(resultados)
            tag=tags[resultadosindices]

            for tagaux in datos["contenido"]:
                if tagaux["tag"]== tag:
                    respuesta = tagaux["respuesta"]

            elemento2=cols[2].selectbox("Ingrese el elemento:", ("Elemento 2","hidrogeno", "oxigeno", "carbono","nitrogeno","fosforo","azufre","selenio","fluor","cloro","bromo","yodo","astato"), key = "optelement2")
            prefijo2=int(cols[3].selectbox("Valencia 2",(-3,-2,-1,1,2,3,4,5,6,7,8,9), key = "_prefijo2"))
            cubeta2= [0 for _ in range(len(palabras))]
            entradaprocesada2= nltk.word_tokenize(elemento2)
            entradaprocesada2 =[stemmer.stem(palabra.lower()) for palabra in entradaprocesada2]
            for palabraindividual2 in entradaprocesada2:
                for i, palabra in enumerate(palabras):
                    if palabra == palabraindividual2:
                        cubeta2[i] = 1
            resultados2 = modelo.predict([numpy.array(cubeta2)])
            resultadosindices2= numpy.argmax(resultados2)
            tag2=tags[resultadosindices2]

            for tagaux in datos["contenido"]:
                if tagaux["tag"]== tag2:
                    respuesta2 = tagaux["respuesta"]

            elemento3=cols[4].selectbox("Ingrese el elemento:", ('ninguno', 'agua'), key = "optelement3")
            prefijo3=int(cols[5].selectbox("Valencia 3",(-3,-2,-1,1,2,3,4,5,6,7,8,9), key = "_prefijo3"))
            cubeta3= [0 for _ in range(len(palabras))]
            entradaprocesada3= nltk.word_tokenize(elemento3)
            entradaprocesada3 =[stemmer.stem(palabra.lower()) for palabra in entradaprocesada3]
            for palabraindividual3 in entradaprocesada3:
                for i, palabra in enumerate(palabras):
                    if palabra == palabraindividual3:
                        cubeta3[i] = 1
            resultados3 = modelo.predict([numpy.array(cubeta3)])
            resultadosindices3= numpy.argmax(resultados3)
            tag3=tags[resultadosindices3]

            for tagaux in datos["contenido"]:
                if tagaux["tag"]== tag3:
                    respuesta3 = tagaux["respuesta"]
        

            def obtsimbolo(simb):
               # simboloq=df[df['nombre']==simb]['simbolo']
                dfSearchedElement = df['simbolo'].where(df['nombre']==simb)
                dfSearchedElement.dropna(inplace=True)
                return dfSearchedElement.squeeze()
            
            def obtprefijo(simb):
               # simboloq=df[df['nombre']==simb]['simbolo']
                df2SearchedElement = df2['Prefijo'].where(df2['Numero']==simb)
                df2SearchedElement.dropna(inplace=True)
                return df2SearchedElement.squeeze()
            
            def obtraiz(simb):
               # simboloq=df[df['nombre']==simb]['simbolo']
                dfSearchedElement = df['raiz'].where(df['nombre']==simb)
                dfSearchedElement.dropna(inplace=True)
                return dfSearchedElement.squeeze()
            
            
            lentrada=[]
            for i in respuesta:
                lentrada.append(respuesta)

            for i in respuesta2:
                lentrada.append(respuesta2)

            for i in respuesta3:
                lentrada.append(respuesta3)
                
            #Filtro valor absoluto:
                        
            vprefijo1= int(prefijo1)
            vprefijo2= int(prefijo2)
            vprefijo3= int(prefijo3)            
            
            prefijo1m = abs(vprefijo1)
            prefijo2m = abs(vprefijo2)
            prefijo3m = abs(vprefijo3)            
                       
            def numpar(val):
                valp= val%2
                return valp
            
            def valpar(val1,val2):
                global prefijopar1, prefijopar2
                valres=val2/val1
                valfin=val2/valres
                prefijopar1=val1/valfin
                prefijopar2=val2/valfin
                return prefijopar1, prefijopar2
                
            def valparinv(val1,val2):
                global prefijopar1, prefijopar2
                valres=val1/val2
                valfin=val1/valres
                prefijopar1=val1/valfin
                prefijopar2=val2/valfin
                return prefijopar1, prefijopar2            

            lhidruros=[['metal'], ['hidrogeno'],['ninguno']]
            loxidosm=[['metal'],['oxigeno'],['ninguno']]
            lhidroxidos=[['metal'],['oxigeno'],['agua']]
            lsalesbi=[['metal'],['no metal'],['ninguno']]
            lhidracidos=[['no metal'],['hidrogeno'],['ninguno']]
            lanhidridos=[['no metal'],['oxigeno'],['ninguno']]
            
            cols[6].text("")
            cols[6].image("arrow.jpg")
            
            st.markdown("""
                    <style>
                    .big-font2 {
                        font-size:45px !important;
                    }
                    </style>
                    """, unsafe_allow_html=True)
            
            
            if lentrada==lhidruros:
                if prefijo1m == 1:
                        del prefijo1m
                        prefijo1m= ""

                if prefijo2m == 1:
                    del prefijo2m
                    prefijo2m= ""
                rhidruro = (f"{obtsimbolo(elemento)}{prefijo2m}{obtsimbolo(elemento2)}{prefijo1m}")
                    
                cols[7].text("")
                cols[7].markdown(f'<p class="big-font2">{rhidruro}</p>', unsafe_allow_html=True)
                nomen1 = (f"{obtprefijo(prefijo1)}-hidruro de {elemento}")
                st.markdown(f'<p class="big-font2">{nomen1}</p>', unsafe_allow_html=True)
                st.subheader("Hidruros:")
                st.text("""
                - Los hidruros de los metales alcalinos (grupo I), alcalinot??rreos (grupo II) y de algunos otros elementos del sistema peri??dico se forman directamente de los elementos a temperaturas elevadas.
                - Otros pueden ser formados por intercambio del ani??n.
                - Algunos hidruros de los elementos nobles se pueden formar tambi??n aprovechando el hidr??geno del metanol.
                - Por lo general los hidruros son compuestos estequiom??tricos que presentan propiedades met??licas como por ejemplo la conductividad.
                - Tienen una gran velocidad de difusi??n del hidr??geno por medio del s??lido cuando se someten a temperatura elevadas.
                - Los hidruros salinos por lo general se encuentran en estado s??lido y son de color blanco o gris.
                - Este tipo de hidruro se puede obtener por medio de reacciones directas del metal con el hidr??geno.
                - Elementos como el f??sforo, ars??nico y sus compuestos son considerados t??xicos.
                - Tienen agentes reductores bastante efectivos y no reaccionan con el agua o con los ??cidos catalogados como no oxidantes.
                    """)
                st.image("hidruros.jpg", width = 500)
                                       

            elif lentrada==loxidosm:
                resta= numpar(prefijo1m)- numpar(prefijo2m)                
                if (resta== 0) and (prefijo1m > prefijo2m):
                    prefijopar1, prefijopar2 = valparinv(prefijo1m, prefijo2m)
                    prepar1int = int(prefijopar1)
                    prepar2int = int(prefijopar2)
                    if prepar1int == 1:
                        del prepar1int
                        prepar1int= ""

                    if prepar2int == 1:
                        del prepar2int
                        prepar2int= ""
                    roxido = (f"{obtsimbolo(elemento)}{prepar2int}{obtsimbolo(elemento2)}{prepar1int}")
                    nomen2 = (f"{obtprefijo(prefijopar1)}-oxido de {obtprefijo(prefijopar2)}-{elemento}")
                        
                elif (resta == 0) and (prefijo1m < prefijo2m):
                    prefijopar1, prefijopar2= valpar(prefijo1m, prefijo2m)
                    prepar1int = int(prefijopar1)
                    prepar2int = int(prefijopar2)
                    if prepar1int == 1:
                        del prepar1int
                        prepar1int= ""

                    if prepar2int == 1:
                        del prepar2int
                        prepar2int= ""
                    roxido = (f"{obtsimbolo(elemento)}{prepar2int}{obtsimbolo(elemento2)}{prepar1int}")
                    nomen2 = (f"{obtprefijo(prefijopar1)}-oxido de {obtprefijo(prefijopar2)}-{elemento}")
                        
                elif (resta== 0) and (prefijo1m == prefijo2m):
                    prefijopar1, prefijopar2 = valparinv(prefijo1m, prefijo2m)
                    prepar1int = int(prefijopar1)
                    prepar2int = int(prefijopar2)
                    if prepar1int == 1:
                        del prepar1int
                        prepar1int= ""

                    if prepar2int == 1:
                        del prepar2int
                        prepar2int= ""
                    roxido = (f"{obtsimbolo(elemento)}{prepar2int}{obtsimbolo(elemento2)}{prepar1int}")
                    nomen2 = (f"oxido de {elemento}")
                        
                else:
                    if prefijo1m == 1:
                        del prefijo1m
                        prefijo1m= ""

                    if prefijo2m == 1:
                        del prefijo2m
                        prefijo2m= ""
                    roxido = (f"{obtsimbolo(elemento)}{prefijo2m}{obtsimbolo(elemento2)}{prefijo1m}")
                    nomen2 = (f"{obtprefijo(prefijo1)}-oxido de {obtprefijo(prefijo2)}-{elemento}")
                    
                cols[7].text("")
                cols[7].markdown(f'<p class="big-font2">{roxido}</p>', unsafe_allow_html=True)
                #nomen2 = (f"{obtprefijo(prefijo1)}-oxido de {obtprefijo(prefijo2)}-{elemento}")
                st.markdown(f'<p class="big-font2">{nomen2}</p>', unsafe_allow_html=True)
                st.subheader("Oxidos Metalicos:")
                st.text("""
                - Son combinaciones binarias de un metal con el ox??geno, en las que el ox??geno tiene n??mero de oxidaci??n (-2.)
                - Poseen basicidad la cual es la capacidad que tiene una sustancia de ser ??cido neutralizante cuando se encuentra en una soluci??n de tipo acuosa.
                - Tiene anfoterismo, en este aspecto se debe recordar que no todos los ??xidos son iguales por lo que mientras est?? ubicado m??s hacia la izquierda, el metal ser?? m??s b??sico que el ??xido.
                - Por lo general, tienden a ser s??lidos.
                - Tienen un punto de fusi??n relativamente alto.
                - Son cristalinos en su gran mayor??a y, adem??s, son medianamente solubles en agua.
                - Son buenos conductores de la electricidad.
                - Pueden estar presentes en los tres diferentes estados de agregaci??n de la materia.
                - Son compuestos de tipo inorg??nico.
                - El proceso para que se obtengan depende en gran manera de la naturaleza del metal o de la reactividad y de las condiciones f??sicas que le rodean.
               """)
                st.image("oxidos.jpg", width = 500)

            elif lentrada==lhidroxidos:
                if prefijo1m == 1:
                        del prefijo1m
                        prefijo1m= ""
                rhidroxido= (f"{obtsimbolo(elemento)}(OH){prefijo1m}")
                cols[7].text("")
                cols[7].markdown(f'<p class="big-font2">{rhidroxido}</p>', unsafe_allow_html=True)
                nomen3 = (f"{obtprefijo(prefijo1)}-hidroxido de {elemento}")
                st.markdown(f'<p class="big-font2">{nomen3}</p>', unsafe_allow_html=True)
                st.subheader("Hidroxidos:")
                st.text("""
                - Los hidr??xidos son un tipo de compuesto qu??mico que est?? formado a partir de la uni??n de un elemento de tipo met??lico o cati??nico con un elemento que pertenece al grupo de los hidr??xidos, o aniones.
                - Se caracterizan por ser compuestos inorg??nicos ternarios porque tienen en su mol??cula de hidr??geno, una mol??cula de ox??geno y un elemento de tipo met??lico.
                - Pueden desasociarse cuando se disuelven en agua. Tienen un car??cter b??sico bastante fuerte porque el grupo hidroxilo tiene la capacidad de captar protones.
                - Pueden hacer que el color del papel tornasol de un tono rojo a uno azul.
                - Tienen la capacidad de reaccionar con los ??cidos y producir de esta manera una sal y agua.
                - Cuando hacer alg??n tipo de reacci??n puede liberar energ??a.
                        """)
                st.image("hidroxidos.jpg", width = 500)

            elif lentrada==lsalesbi:
                resta= numpar(prefijo1m)- numpar(prefijo2m)                
                if (resta== 0) and (prefijo1m > prefijo2m):
                    prefijopar1, prefijopar2 = valparinv(prefijo1m, prefijo2m)
                    prepar1int = int(prefijopar1)
                    prepar2int = int(prefijopar2)
                    if prepar1int == 1:
                        del prepar1int
                        prepar1int= ""

                    if prepar2int == 1:
                        del prepar2int
                        prepar2int= ""
                    rsalesbi =(f"{obtsimbolo(elemento)}{prepar2int}{obtsimbolo(elemento2)}{prepar1int}")
                    nomen4 = (f"{obtprefijo(prefijopar1)}-{obtraiz(elemento2)}uro de {obtprefijo(prefijopar2)}-{elemento}")
                        
                elif (resta == 0) and (prefijo1m < prefijo2m):
                    prefijopar1, prefijopar2= valpar(prefijo1m, prefijo2m)
                    prepar1int = int(prefijopar1)
                    prepar2int = int(prefijopar2)
                    if prepar1int == 1:
                        del prepar1int
                        prepar1int= ""

                    if prepar2int == 1:
                        del prepar2int
                        prepar2int= ""
                    rsalesbi =(f"{obtsimbolo(elemento)}{prepar2int}{obtsimbolo(elemento2)}{prepar1int}")
                    nomen4 = (f"{obtprefijo(prefijopar1)}-{obtraiz(elemento2)}uro de {obtprefijo(prefijopar2)}-{elemento}")
                        
                elif (resta== 0) and (prefijo1m == prefijo2m):
                    prefijopar1, prefijopar2 = valparinv(prefijo1m, prefijo2m)
                    prepar1int = int(prefijopar1)
                    prepar2int = int(prefijopar2)
                    if prepar1int == 1:
                        del prepar1int
                        prepar1int= ""

                    if prepar2int == 1:
                        del prepar2int
                        prepar2int= ""
                    rsalesbi =(f"{obtsimbolo(elemento)}{prepar2int}{obtsimbolo(elemento2)}{prepar1int}")
                    nomen4 = (f"{obtraiz(elemento2)}uro de {elemento}")
                    
                        
                else:
                    if prefijo1m == 1:
                        del prefijo1m
                        prefijo1m= ""

                    if prefijo2m == 1:
                        del prefijo2m
                        prefijo2m= ""
                    rsalesbi =(f"{obtsimbolo(elemento)}{prefijo2m}{obtsimbolo(elemento2)}{prefijo1m}")
                    nomen4 = (f"{obtprefijo(prefijo1)}-{obtraiz(elemento2)}uro de {obtprefijo(prefijo2)}-{elemento}")
                
                cols[7].text("")
                cols[7].markdown(f'<p class="big-font2">{rsalesbi}</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="big-font2">{nomen4}</p>', unsafe_allow_html=True)
                st.subheader("Sales Binarias:")
                st.text("""
                - Una sal binaria es una combinaci??n que se hace entre un metal y un no metal en su estructura y que poseen adem??s una f??rmula qu??mica general como MmXn, donde M ser?? el elemento met??lico mientras que X el no met??lico.
                - Tienen cierta semejanza con la sal de cocina.
                - Son tambi??n conocidas con el nombre de sales neutras.
                - Tienen una consistencia s??lida, son muy cristalinas y por lo general su color es blanco.
                - Posee un sabor salado.
                - Gran parte de las sales binarias son solubles cuando entran en contacto con el agua.
                - En las sales binarias el elemento no met??lico siempre actuar?? con su valencia fija frente al hidr??geno.
                - Es uno de los tres tipos de sales que se pueden encontrar en la naturaleza.
                - El no metal que forma parte de las sales binarias siempre utilizar?? su menor valencia.
                - Son consideradas como parte fundamental de la qu??mica, principalmente en el campo educativo.""")
                st.image("salesbi.jpg", width = 500)

            elif lentrada==lhidracidos:
                if prefijo1m == 1:
                        del prefijo1m
                        prefijo1m= ""
                rhidracido= (f"H{prefijo1m}{obtsimbolo(elemento)}")
                cols[7].text("")
                cols[7].markdown(f'<p class="big-font2">{rhidracido}</p>', unsafe_allow_html=True)
                nomen5 = (f"{obtraiz(elemento)}uro de {obtprefijo(prefijo1)}-hidrogeno")
                st.markdown(f'<p class="big-font2">{nomen5}</p>', unsafe_allow_html=True)
                st.subheader("Hidracidos:")
                st.text("""
                -Tambi??n son conocidos como ??cidos hidr??cidos, sales binarias o h??dricos ??cidos, est??n hechos por dos compuestos binarios ??cidos los cuales deben ser un hidr??geno
                (del grupo hal??geno o ant??geno en la tabla peri??dica) y un no metal, sin presencia de ox??geno.
                -Cuando se disuelven en agua son solubles.
                -No poseen ox??geno en su composici??n.
                -Liberan usualmente un muy denso humo blanco.
                -Cuando se encuentran en su estado natural son gaseosos y para nombrarlos se utiliza el nombre del no metal con la terminaci??n uro y seguido del nombre Hidr??geno.
                -Se obtienen tambi??n por disoluci??n acuosa.
                -Son perfectos cuando se utilizan como conductor de energ??a el??ctrica.
                -Con respecto a su aspecto ??stos son incoloros, son soluciones transparentes.
                -Tambi??n cuando entran en contacto con agua originan soluciones ??cidas.
                -Solo existen sietes ??cidos hidr??cidos que forman solo con los no metales de Cl, S, I, F, Se, Te.
                -Sus puntos de ebullici??n son superiores a la de los anh??dridos, por ejemplo, el Cloruro de Hidr??geno hierve a -85Co pero el ??cido Clorh??drico hierve a -48Co.
                        """)
                st.image("hidracidos.jpg", width = 500)              


            elif lentrada==lanhidridos:
                resta= numpar(prefijo1m)- numpar(prefijo2m)                
                if (resta== 0) and (prefijo1m > prefijo2m):
                    prefijopar1, prefijopar2 = valparinv(prefijo1m, prefijo2m)
                    prepar1int = int(prefijopar1)
                    prepar2int = int(prefijopar2)
                    if prepar1int == 1:
                        del prepar1int
                        prepar1int= ""

                    if prepar2int == 1:
                        del prepar2int
                        prepar2int= ""
                    ranhidrido = (f"{obtsimbolo(elemento)}{prepar2int}O{prepar1int}")
                        
                elif (resta == 0) and (prefijo1m < prefijo2m):
                    prefijopar1, prefijopar2= valpar(prefijo1m, prefijo2m)
                    prepar1int = int(prefijopar1)
                    prepar2int = int(prefijopar2)
                    if prepar1int == 1:
                        del prepar1int
                        prepar1int= ""

                    if prepar2int == 1:
                        del prepar2int
                        prepar2int= ""
                    ranhidrido = (f"{obtsimbolo(elemento)}{prepar2int}O{prepar1int}")
                        
                elif (resta== 0) and (prefijo1m == prefijo2m):
                    prefijopar1, prefijopar2 = valparinv(prefijo1m, prefijo2m)
                    prepar1int = int(prefijopar1)
                    prepar2int = int(prefijopar2)
                    if prepar1int == 1:
                        del prepar1int
                        prepar1int= ""

                    if prepar2int == 1:
                        del prepar2int
                        prepar2int= ""
                    ranhidrido = (f"{obtsimbolo(elemento)}{prepar2int}O{prepar1int}") 
                        
                else:
                    if prefijo1m == 1:
                        del prefijo1m
                        prefijo1m= ""

                    if prefijo2m == 1:
                        del prefijo2m
                        prefijo2m= ""
                    ranhidrido = (f"{obtsimbolo(elemento)}{prefijo2m}O{prefijo1m}")
                
                cols[7].text("")
                cols[7].markdown(f'<p class="big-font2">{ranhidrido}</p>', unsafe_allow_html=True)
                nomen6 = (f"{obtprefijo(prefijo1)}-oxido de {obtprefijo(prefijo2)}-{elemento}")
                st.markdown(f'<p class="big-font2">{nomen6}</p>', unsafe_allow_html=True)
                st.subheader("Anhidridos:")
                st.text("""
                -En qu??mica podemos definir los anh??dridos como un compuestos qu??micos de tipo binario que surgen al juntar un No Metal con Ox??geno,
                tambi??n son llamados como ??xidos No Met??licos u ??xidos ??cidos, cuya f??rmula general es (RCO)2??.
                -Son productos de la condensaci??n de 2 mol??culas de ??cidos carbox??licos. 
                -La f??rmula de los anh??dridos es del tipo X2On (donde X es un elemento no met??lico y O es ox??geno) Ejemplos: SeO, So3, CO2. Poseen la caracter??stica de ser especialmente reactivos.
                -Se pueden manejar en muchas ??reas, lo habitual, donde son m??s vistos y usados es en la fabricaci??n de medicamentos.
                -Como por ejemplo en el ??mbito medico existe uno muy usado llamado ??cido Acetilsalic??lico un f??rmaco que es muy utilizado.
                -Como ya se ha mencionado vienen a ser fruto de la deshidrataci??n de dos mol??culas, pero tambi??n existen casos donde pudiese ser una, en el caso intramolecular, de ??cido carbox??lico.
                -Tambi??n son llamados anh??dridos carbox??licos.
                """)
                st.image("anhidridos.jpg", width = 500)              

            else:
                cols[7].text("La reaccion no esta disponible")    
                
            mt3, val, mt4 = st.columns([1,5,2])
            
            with mt3:
                st.text("")
                
            with val:
                st.subheader("Tabla de Valencias:")
                st.image('valencias.png')
                
            with mt4:
                st.text("")               
                
            st.text("")
            st.text("")
                        
            with st.expander("Acerca De"):
                st.write(f"""
                La aplicacion es capaz de determinar reacciones quimicas inorganicas como se muestra a continuacion:

                Hidruros:

                Metal + Hidrogeno + Ninguno -----> Reaccion Hidruro

                Oxido Metalicos:

                Metal + Oxigeno + Ninguno -----> Reaccion Oxido Met??lico

                Hidroxido:

                Metal + Oxigeno + Agua -----> Reaccion Hidroxido

                Sales Binarias:

                Metal + No metal + Ninguno -----> Reaccion Sal Binaria

                Hidracidos:

                No metal + Hidrogeno + Ninguno -----> Reaccion Hidracido

                Anhidridos:

                No metal + Oxigeno + Ninguno -----> Reaccion Anhidrido



                """)

            with st.expander("Reaccion Quimica"):
                st.write(f"""
            Las reacciones qu??micas (tambi??n llamadas cambios qu??micos o fen??menos qu??micos) son procesos termodin??micos de transformaci??n de la materia. En estas reacciones intervienen dos o m??s sustancias (reactivos o reactantes), que cambian significativamente en el proceso, y pueden consumir o liberar energ??a para generar dos o m??s sustancias llamadas productos.
            Toda reacci??n qu??mica somete a la materia a una transformaci??n qu??mica, alterando su estructura y composici??n molecular (a diferencia de los cambios f??sicos que s??lo afectan su forma o estado de agregaci??n). Los cambios qu??micos generalmente producen sustancias nuevas, distintas de las que ten??amos al principio.

            Cambios f??sicos y qu??micos en la materia :

            Mientras que cambios f??sicos de la materia son aquellos que alteran su forma sin cambiar su composici??n, los cambios qu??micos alteran la distribuci??n y los enlaces de los ??tomos de la materia, logrando que se combinen de manera distinta obteni??ndose as?? sustancias diferentes a las iniciales.

            Como se representa una reacci??n qu??mica:

            Las reacciones qu??micas se representan mediante ecuaciones qu??micas, es decir, f??rmulas en las que se describen los reactivos participantes y los productos obtenidos

            La forma general de representar una ecuaci??n qu??mica es:

            aA + bB ----> cC + dD

            Donde:

            ???	A y B son los reactivos.

            ???	C y D son los productos.

            ???	a, b, c y d son los coeficientes estequiom??tricos (son n??meros que indican la cantidad de reactivos y productos) que deben ser ajustados de manera que haya la misma cantidad de cada elemento en los reactivos y en los productos. De esta forma se cumple la Ley de Conservaci??n de la Materia.  
                            """)

            with st.expander("Enlace Quimico"):
                st.write("""
                Un enlace qu??mico es la fuerza que une a los ??tomos para formar compuestos qu??micos. Esta uni??n le confiere estabilidad al compuesto resultante. La energ??a necesaria para romper un enlace qu??mico se denomina energ??a de enlace.
                En este proceso los ??tomos ceden o comparten electrones de la capa de valencia, y se unen constituyendo nuevas sustancias homog??neas (no mezclas), inseparables a trav??s de mecanismos f??sicos como el filtrado o el tamizado.
                Existen tres tipos de enlace qu??mico conocidos, dependiendo de la naturaleza de los ??tomos involucrados:

                ???	Enlace covalente. Ocurre entre ??tomos no met??licos y de cargas electromagn??ticas semejantes (por lo general altas), que se unen y comparten algunos pares de electrones de su capa de valencia. Es el tipo de enlace predominante en las mol??culas org??nicas y puede ser de tres tipos: simple (A-A), doble (A=A) y triple (A???A), dependiendo de la cantidad de electrones compartidos.

                ???	Enlace i??nico. Consiste en la atracci??n electrost??tica entre part??culas con cargas el??ctricas de signos contrarios llamadas iones (part??cula cargada el??ctricamente, que puede ser un ??tomo o mol??cula que ha perdido o ganado electrones, es decir, que no es neutro).

                ???	Enlace met??lico. Se da ??nicamente entre ??tomos met??licos de un mismo elemento, que por lo general constituyen estructuras s??lidas, sumamente compactas. Es un enlace fuerte, que une los n??cleos at??micos entre s??, rodeados de sus electrones como en una nube.

                """)

            with st.expander("Elementos"):
                st.write("""
                -Metales 

                En el ??mbito de la qu??mica, se conocen como metales o met??licos a aquellos elementos de la Tabla Peri??dica que se caracterizan por ser buenos conductores de la electricidad y del calor. Estos elementos tienen altas densidades y son generalmente s??lidos a temperatura ambiente (excepto el mercurio). Muchos, adem??s, pueden reflejar la luz, lo cual les otorga su brillo caracter??stico.

                Los metales son los elementos m??s numerosos de la Tabla Peri??dica y algunos forman parte de los m??s abundantes de la corteza terrestre. Una parte de ellos suele hallarse en estado de mayor o menor pureza en la naturaleza, aunque la mayor??a forma parte de minerales del subsuelo terrestre y deben ser separados por el ser humano para utilizarlos.

                -No metales 

                Los no metales son elementos poco abundantes en la Tabla Peri??dica, y se caracterizan por no ser buenos conductores del calor, ni de la electricidad. Sus propiedades son muy distintas a las de los metales. Por otra parte, forman enlaces covalentes para formar mol??culas entre ellos.

                Los elementos esenciales para la vida forman parte de los no metales (ox??geno, carbono, hidr??geno, nitr??geno, f??sforo y azufre). Estos elementos no met??licos tienen propiedades y aspectos muy diversos: pueden ser s??lidos, l??quidos o gaseosos a temperatura ambiente.

                """)

            with st.expander("Valencias"):
                st.write(""" 

                En qu??mica, hablamos de valencia para referirnos al n??mero de electrones que un ??tomo de un elemento qu??mico determinado posee en su ??ltimo nivel de energ??a. Otra forma de interpretar la valencia es como el n??mero de electrones que un ??tomo de un determinado elemento qu??mico debe ceder o aceptar para completar su ??ltimo nivel de energ??a. Estos electrones son de especial relevancia, pues son los responsables de la formaci??n de los enlaces qu??micos, por ejemplo, los enlaces covalentes (covalente: comparten valencia). Son estos electrones los que intervienen en las reacciones qu??micas.

                Existen dos tipos distintos de valencia:

                ???	Valencia positiva m??xima. Refleja la m??xima capacidad combinatoria de un ??tomo, es decir, la mayor cantidad de electrones que puede ceder. Los electrones tienen carga negativa, as?? que un ??tomo que los cede obtiene una valencia positiva (+).

                ???	Valencia negativa. Representa la capacidad de un ??tomo de combinarse con otro que presente valencia positiva. Los ??tomos que reciben electrones presentan una valencia negativa (-).
                """)

            with st.expander("Probabilidades"):
                st.write(f"""
            Las cantidades que se muestran a continuacion representan las probabilidaddes que determina el programa con la finalidad de establecer
            el tipo de elemento que se asigno en la parte superior de la pagina:
            El orden de los numeros representan: (Agua, Hidroxido, Metal, No metal y Oxigeno, respectivamente)

            {lentrada}

            Primer elemento:

            {resultados}

            Segundo elemento:

            {resultados2}

            Tercer elemento:

            {resultados3}""")

            with st.expander("Bibliograf??a"):
                st.write(f"""
                Fuente: https://concepto.de/reaccion-quimica/#ixzz7S0qhaIu5

                Fuente: https://concepto.de/enlace-quimico/#ixzz7S0pvYxKK

                Fuente: https://concepto.de/metales/#ixzz7S0pFOklo

                Fuente: https://concepto.de/no-metales/#ixzz7S0okhvvP

                Fuente: https://concepto.de/valencia-en-quimica/#ixzz7S0oYxT8r""")

            
                
    except Exception as er: 
        print("error: ", er)
mainbot()  

