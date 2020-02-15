# Procedimiento para crear los conjuntos de entrenamiento

**Lo siguiente se ejecuta en una consola interactiva de python**.

**Esto debe de ejecutarse después de etiquetar los datos (ver README_LABELING)**.

1. Importar los siguientes módulos.

```python
import json
import datasets as dat
import indicadores as ind
```

2. Leer los datos del CSV de Yahoo Finance.

```python
data = ind.leeTabla(path_to_csv_file)
```

3. Leer el archivo ```json``` con el diccionario utilizado para calcular los indicadores técnicos.

```python
f = open(path_to_json_file)
dicc = json.load(f)
f.close()
```

4. Utilizar la función ```dat.creaEntrenamiento```

```python
dat.creaEntrenamiento(data, dicc, arch_eti, ruta_eti, ruta_dest, activo)
```
en donde:

* ```data``` es un pandas dataframe con los datos del CSV de  Yahoo Finance.

* ```dicc``` es un diccionario que contiene los parámetros de cada indicador técnico.

* ```arch_eti``` es un string que contiene la ruta del archivo CSV que contiene el nombre de cada conjunto etiquetado (ver el archivo archivos_etiquetados.csv)

* ```ruta_eti``` es un string que especifica la ruta de la carpeta que contiene los conjuntos de datos etiquetados.

* ```ruta_dest``` es un string que indica la ruta de la carpeta en donde se guardarán los archivos de entrenamiento.

* ```activo```es un string que se utiliza como prefijo para el nombre de cada archivo de entrenamiento.
