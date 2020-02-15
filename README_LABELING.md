# Procedimiento para etiquetar los datos

**Lo siguiente se ejecuta en una consola interactiva de python**.

1. importar los siguientes módulos

```python
import datasets as dat
import indicadores as ind
```

2. Leer los datos del CSV de Yahoo Finance

```python
data = ind.leeTabla(path_to_csv_file)
```

3. Crea los bloques que se etiquetarán

```python
blocks = dat.separaBloques(data, block_size, start_date) #Bloques sin traslape
blocks = dat.bloquesDeslizantes(datos, block_size, window_size, start_date) #Bloques con traslape
```
en donde:

* ```block_size``` es un entero que especifíca el tamaño de cada bloque.

* ```start_date``` es una cadena con formato 'YYYY-MM-DD' que indica la fecha de inicio.

* ```window_size``` es un entero que especifica el tamaño de la ventanada deslizante (únicamente para bloques con traslape).

4. Inicia el proceso de etiquetado (esto puede tardar bastante tiempo, depende de los parámetros).

```python
lab_blocks = dat.etiquetaBloques(blocks,numGen ,popSize , flagOper, clean, execPrice, execStep)
```
en donde:

* ```numGen``` es un entero que especifica el número de generaciones (sugerencia: 30).

* ```popSize``` es un entero que especifica es tamaño de la población (sugerencia: 50).

* ```flagOper``` es un booleano que especifica si el número de transacciones debe de considerarse (sugerencia: True).

* ```clean``` es un booleano que especifica si las señales repetidas consecutivas deben de eliminarse (sugerencia: Establecer como ```True``` ya que se trabaja con el supuesto de comprar/vender todo lo posible).

* ```execPrice``` string que especifica el tipo de precio de ejecición:
    - 'open': Precio de apertura.
    - 'mid': Precio mid (promedio de máximo y mínimo).
    - 'adj.close': Cierre ajustado.
    - 'close': Cierre.

* ```h``` es un entero que indica el momento de ejecución después de recibir una señala. Por ejemplo si la señal se recibe en el tiempo $t$ y $h = 1$, entonces el precio de ejecución se calcula con los precios de  $t + h = t + 1$ (sugerencia h = 1).

5. Guarda los datos etiquetados

```python
dat.guardaCSV(lab_blocks, folder_path, prefix)
```
en donde: 

* ```lab_blocks``` es una lista con los bloques etiquetados.

* ```folder_path``` es un string con la ruta del folder en donde se guardarán los datos etiquetados.

* ```prefix``` es una cadena auxiliar para establecer un prefijo al nombre de cada archivo.