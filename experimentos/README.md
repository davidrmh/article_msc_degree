# Experimentos

**NOTA:** Es necesario conservar la estructura y ubicación de los archivos (no me esmeré en hacer tan robusto el código :-p)


1. Para cada metodología (AQ o CN2) debe de haber una carpeta propia. Adentro de dicha carpeta, se crean carpetas correspondientes a cada experimento y adentro de cada una de ellas deben de crearse dos carpetas ```log``` y ```reglas```.

2. Para cada metodología, hay un archivo con código en ```R```, por ejemplo, ```AQ.R```. Este archivo contiene un conjunto de variables globales que necesitan modificarse, así como una función ```main``` que inicia el proceso de aprendizaje.

**EJEMPLO**

1. Abrir ```AQ.R``` dentro la carpeta ```AQ``` (de preferencia utilizar Rstudio).

2. Ajustar las variables globales ```
arch_csv #Revisar archivo entrena_prueba.csv
ruta_entrena #carpeta en donde están los archivos de entrenamiento
ruta_prueba  #carpeta en donde están los archivos prueba (sugerencia: misma ruta que ruta_entrena)
ruta_etiqueta #carpeta en donde están los archivos etiquetados (sugerencia: ~/data/labeling)
glob_bandaSuperior #Número positivo que representa el porcentaje mínimo que se desea ganar por una venta.
glob_bandaInferior #número negativo que representa el porcentaje de tolerancia a las pérdidas
glob_tipoEjec #Tipo de precio de ejecución
glob_h #parámetro para indicar el momento $t + h$ en donde se ejecuta la señal dada en $t$.
```

2. Ejecutar la función ```AQ.main``` con sus respectivos parámetros.


