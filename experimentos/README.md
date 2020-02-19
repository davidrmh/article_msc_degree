# Experimentos

**NOTA:** Es necesario conservar la estructura y ubicación de los archivos (no me esmeré en hacer tan robusto el código :-p)


1. Para cada metodología (AQ o CN2) debe de haber una carpeta propia. Adentro de dicha carpeta, se crean carpetas correspondientes a cada experimento y adentro de cada una de ellas deben de crearse dos carpetas ```log``` y ```reglas```.

2. Para cada metodología, hay un archivo con código en ```R```, por ejemplo, ```AQ.R```. Este archivo contiene un conjunto de variables globales que necesitan modificarse, así como una función ```main``` que inicia el proceso de aprendizaje.

**EJEMPLO**

1. Abrir ```AQ.R``` dentro la carpeta ```AQ``` (de preferencia utilizar Rstudio).

2. Ajustar las variables globales 
   * ```arch_csv #Revisar archivo entrena_prueba.csv```
   * ```ruta_entrena #carpeta en donde están los archivos de entrenamiento```
   * ``` ruta_prueba  #carpeta en donde están los archivos prueba (sugerencia: misma ruta que ruta_entrena)```
   * ``` ruta_etiqueta #carpeta en donde están los archivos etiquetados (sugerencia: ~/data/labeling)```
   * ```glob_bandaSuperior #Número positivo que representa el porcentaje mínimo que se desea ganar por una venta.```
   * ```glob_bandaInferior #número negativo que representa el porcentaje de tolerancia a las pérdidas```
   * ```glob_tipoEjec #Tipo de precio de ejecución```
   * ```glob_h #parámetro para indicar el momento $t + h$ en donde se ejecuta la señal dada en $t$.```

2. Ejecutar la función ```AQ.main``` con sus respectivos parámetros.

# Evaluación de resultados

1. Con los archivos generados en los experimentos, actualizar el archivo ```arch_evaluar.csv```, este archivo contiene la lista de archivos que contienen las predicciones para cada período de prueba.

2. **En una sesión interactiva de python** importar el módulo ```metricas```
```python
import metricas as met
```

3. Utilizar la función ```evaluaMetrica``` con los parámetros deseados.

```python
met.evaluaMetrica(...)
```

# Observaciones

## Sobre el ordenamiento de las reglas:

* La primera vez que ordenan las reglas, no existen penalizaciones (o recompensas) por el desempeño de estas, así que
se utiliza la suma (normalizada) ```Laplace + Soporte```.

* Una vez que se tienen penalizaciones (o recompensas), se utilizan estas (normalizadas nuevamente) para ordenar las reglas.

* Ver la función ```ordenaReglas``` del archivo ```evaluaReglas.R``` y ```actualizaLista.R``` del archivo ```auxFun.R```.

## Sobre las posiciones abiertas

* Se vende si hay una ganancia (la que sea) o se cae debajo de la banda inferior (pánico)

* En otro caso la última compra no se considera (NO HAY GANANCIA PERO LA PÉRDIDA ESTÁ DENTRO DEL RIESGO TOLERADO)

## Sobre los archivos log

* Los archivos log incluyen el precio de ejecución considerando el costo de transacción.
