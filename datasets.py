# coding: utf-8

'''
Funciones para crear los conjuntos de prueba y de entrenamiento
'''

import indicadores as ind
import etiqueta as eti
import pandas as pd
import numpy as np
from copy import deepcopy
import os

##==============================================================================
## Función para crear conjuntos de prueba para ventanas deslizantes suaves
##==============================================================================
def bloquesPrueba(archivo = 'sub_bloques.csv', ruta = './data/training/', size = 30, target = 'prueba'):
	'''
	Función para crear conjuntos de entrenamiento utilizando bloques etiquetados
	con una ventana deslizante suave

	ENTRADA
	archivo: string con la ruta del archivo CSV que contiene el nombre de los archivos de cada bloque

	ruta: string con la ruta en donde se almacenan los archivos del archivo CSV.

	size: Entero que representa el tamaño de cada sub bloque.

	target: String con el nombre de la carpeta que se creará y contendrá cada sub bloque
	esta carpeta se crea adentro de la ruta señalada por el parámetro ruta

	SALIDA
	crea un carpeta en ruta + target con los sub bloques creados.
	'''
	#Por seguridad para que los archivos se guarden dentro de la carpeta
	#tiene que ser el nombre de una carpeta (terminar con /)
	if target.find('/') == -1:
		target = target + '/'
	#Crea la carpeta destino
	try:
		os.mkdir(ruta + target)
	except:
		None

	#lee el archivo csv con los nombres de cada bloque
	nombres = pd.read_csv(archivo)

	#Crea parejas entrenamiento - prueba
	n_bloques = nombres.shape[0]
	x1 = nombres['bloque'].iloc[0:(n_bloques - 1)]
	x2 = nombres['bloque'].iloc[1:n_bloques]
	parejas = zip(x1, x2)

	#Para crear el archivo csv utilizado para evaluar
	#los experimentos (archivo entrena_prueba.csv)
	lista_entrena = []
	lista_prueba = []

	#Lee cada bloque
	for pareja in parejas:
		#Abre cada bloque
		nom_bloque1 = pareja[0]
		nom_bloque2 = pareja[1]
		bloque1 = pd.read_csv(ruta + nom_bloque1)
		bloque2 = pd.read_csv(ruta + nom_bloque2)

		#Obtiene fechas (como conjuntos)
		fechas1 = set(bloque1['Date'])
		fechas2 = set(bloque2['Date'])

		#Fechas para el conjunto de prueba
		fechas3 = fechas2 - fechas2.intersection(fechas1)
		fechas3 = list(fechas3)

		#Crea el bloque de prueba
		lista_indices = []
		for i in range(len(bloque2['Date'])):
			if bloque2['Date'][i] in fechas3:
				lista_indices.append(i)

		#slicing
		bloque_prueba = bloque2.iloc[lista_indices,:].reset_index(drop = True)		
		aux = nom_bloque2.replace('.csv','_prueba.csv')
		nom_prueba = ruta + target + aux
		bloque_prueba.to_csv(nom_prueba, index = False)
		print 'Se crea prueba ' + nom_prueba

		lista_entrena.append(nom_bloque1)
		lista_prueba.append(nom_prueba)
	aux_eval = pd.DataFrame({'entrena':lista_entrena, 'prueba':lista_prueba})
	aux_eval.to_csv(ruta + target + 'entrena_prueba.csv', index = False)
	print 'Conjuntos de prueba creados'


##==============================================================================
## Función para separar bloques de una manera deslizante (más suave que la función separaBloques)
##==============================================================================
def bloquesDeslizantes(datos, lon = 90, paso = 1, start = '2013-02-15'):
	'''
	ENTRADA

	datos: Pandas dataframe con los datos del CSV
	(idealmente creado con la función leeTabla del módulo indicadores)

	lon: Entero positivo que representa el número de observaciones de cada bloque

	paso: Entero positivo que representa la magnitud de deslizamiento

	start: String de la forma YYYY-MM-DD que indica la fecha de inicio

	SALIDA
	Lista con los bloques de datos
	'''
	bloques = []

	#índice de inicio
	inicio=datos[datos['Date']==start].index[0]

	#índice fin del primer bloque
	fin = inicio + lon - 1

	#último índice válido
	ultimoIndice = datos.shape[0] - 1

	#Separa los bloques hasta que fin > ultimoIndice
	while fin <= ultimoIndice:
		#Obtiene el bloque correspondiente
		bloque = datos.loc[inicio:fin,:]

		#Reinicia índices
		bloque = bloque.reset_index(drop = True)

		#Agrega a la lista
		bloques.append(bloque)

		#Actualiza índices
		inicio = inicio + paso
		fin = fin + paso

	return bloques	

##==============================================================================
## Función para separar los datos en bloques consecutivos del mismo tamaño
##==============================================================================
def separaBloques(datos, lon = 90, start = '2013-02-15'):
	'''
	ENTRADA

	datos: Pandas dataframe con los datos del CSV
	(idealmente creado con la función leeTabla del módulo indicadores)

	lon: Entero que representa el número de observaciones de cada bloque

	start: String de la forma YYYY-MM-DD que indica la fecha de inicio

	SALIDA
	Lista con los bloques de datos

	'''

	#índice de inicio
	inicio=datos[datos['Date']==start].index[0]

	#número de observaciones
	n_obs = datos.shape[0]

	#número de bloques posibles
	n_bloques = int((n_obs - inicio) / lon)

	#lista para almacenar los bloques
	bloques = []

	for j in range(0, n_bloques):

		#obtiene el bloque j
		bloque =  datos.iloc[inicio + j*lon: (inicio + (j+1)*lon),]

		#Reinicia los índices
		bloque = bloque.reset_index(drop = True)

		#agrega a la lista
		bloques.append(bloque)

	return bloques

##==============================================================================
## Función para etiquetar los bloques creados con separaBloques
##==============================================================================
def etiquetaBloques(bloques,numGen=30,popSize=50, flagOper = True, limpia = True, tipoEjec = 'open', h = 0):
    '''
    Etiqueta los datos utilizando un algoritmo genético que busca
    la combinación de señales compra,venta,hold que generen mayor ganancia

    ENTRADA
    bloques: Lista con los bloques a etiquetar (cada bloque es un pandas dataframe)

    numGen: Entero, número de generaciones.

    popSize: Entero, tamaño de la población.

    flagOper: Booleano. True => Considera el número de transacciones
    False => No considera el número de transacciones

    limpia: Booleano. True => Limpia señales repetidas

    tipoEjec: String que indica el tipo de precio de ejecución (ver función precioEjecucion módulo etiqueta)

    h: Entero positivo que representa el número de periodos en el futuro, a partir de  'fecha', 
    en el cual se calculará el precio de ejecución

    SALIDA
    Lista con los bloques etiquetados
    '''

    bloques_eti = []

    #número de bloques
    n_bloq = len(bloques)

    #auxiliar
    cont = 0

    for bloque in bloques:

    	etiquetado = eti.etiquetaMetodo2(bloque, numGen, popSize, flagOper, limpia, tipoEjec, h)

    	print 50*'='

    	cont = cont + 1

    	print 'Finaliza bloque ' + str(cont) + ' de ' + str(n_bloq)

    	print 50*'='

    	bloques_eti.append(etiquetado)

    return bloques_eti

##==============================================================================
## Función para crear archivos csv a partir de una lista que contiene
## pandas dataframes. Idealmente esta función se utiliza con la lista de
## la función etiquetaBloques
##==============================================================================
def guardaCSV(lista, ruta = '/datasets/', activo = 'naftrac'):
	'''
	ENTRADA

	lista: Lista que contiene los dataframes (deben de contener al menos una columna llamada Date)

	ruta: String con la carpeta en donde se guardarán los csv

	activo: String con el nombre del activo
	'''

	#auxiliar para el nombre de los archivos
	aux = 1
	for bloque in lista:

		#Extrae fecha inicial y fecha final
		n_obs = bloque.shape[0]
		fecha_in = str(bloque.loc[0,'Date']).split(' ')[0]
		fecha_fin = str(bloque.loc[n_obs-1,'Date']).split(' ')[0]

		#Crea el nombre del archivo
		nombre = '_'.join([str(aux), activo, fecha_in, fecha_fin, str(n_obs) ])
		nombre = ruta + nombre + '.csv'

		#Escribe el csv
		bloque.to_csv(path_or_buf = nombre, index = False)

		aux = aux + 1

	return

##==============================================================================
## Función para crear un dataframe con los atributos y las clases
##==============================================================================
def atributosClases(atributos, clases):
	'''
	ENTRADA

	atributos: Pandas dataframe con los atributos, idealmente creado con la
	funcion combinaIndicadores del modulo indicadores

	clases: Pandas dataframe que contiene al menos las columnas Date y Clase
	(idealmente creado con la funcion etiquetaBloques de este modulo)

	SALIDA
	Pandas dataframe con las columnas Date, las columnas del dataframe atributos y la columna Clase
	'''

	#Nombre de los atributos
	nombre_atributos = atributos.columns

	resultado = pd.DataFrame()

	#Agrega columna de fechas
	resultado['Date']  = deepcopy(clases.loc[:,'Date'])

	#Agrega los atributos
	for atributo in nombre_atributos:
		resultado[atributo]  = deepcopy(atributos.loc[:,atributo])

	#Agrega la columna Clase
	resultado['Clase']  = deepcopy(clases.loc[:,'Clase'])

	return resultado

##==============================================================================
## Función para crear los conjuntos de entrenamiento
##==============================================================================
def creaEntrenamiento(datos, dicc, arch_eti = 'archivos_etiquetados.csv', ruta_eti = './datasets/etiquetado/', ruta_dest = './datasets/atributos_clases/', activo = 'naftrac-entrena' ):
	'''
	ENTRADA

	datos: Pandas dataframe con la informacion del CSV de Yahoo Finance. Creado con
	la funcion leeTabla del modulo indicadores

    dicc: Un diccionario de la forma
    dicc[key] = {'tipo':'FUNCION','parametros':{'window':10,...}}
    en donde FUNCIÓN corresponde al nombre de alguna de las funciones
    para calcular un indicador en particular.
    parametros es un diccionario con los parámetros del indicador de interés

    arch_eti: String con el nombre de archivo CSV que contiene el nombre de
	cada bloque etiquetado (e.g. 1_naftrac-etiquetado_2013-02-15_2013-06-28_90.csv)

    ruta_eti: String con la ruta (sin incluir el nombre del archivo) de los archivos relacionado a lista_arch

    ruta_dest: String con la ruta en donde se guardaran los archivos

	activo: String auxiliar para el nombre del archivo
	'''

	#aquí almaceno cada dataframe que utilizará la función guardarCSV
	entrenamiento = []

	lista_arch = np.array(pd.read_csv(arch_eti, header = None))

	for x in lista_arch:

		archivo = x[0]

		#Nombre del archivo
		nombre_arch = ruta_eti + archivo

		#Abre el archivo con las clases
		clases = pd.read_csv(nombre_arch)

		#Obtiene los atributos
		start = str(clases.loc[0,'Date']).split(' ')[0] #fecha inicial
		n_obs = clases.shape[0] #número de observaciones
		end = str(clases.loc[n_obs - 1,'Date']).split(' ')[0] #fecha final

		lista = ind.creaIndicadores(datos, dicc, start, end)
		atributos = ind.combinaIndicadores(lista)
		entrenamiento.append( atributosClases(atributos, clases) )

		print "Finaliza con archivo" + archivo

	#guarda los archivos
	guardaCSV(entrenamiento, ruta_dest, activo)

	return
