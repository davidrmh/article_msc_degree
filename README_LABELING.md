# Procedure to create the labels in the data

**This is run in an interactive python shell**

1. Import the following modules

```python
import datasets as dat
import indicadores as ind
```

2. Read the data from the csv of Yahoo Finance

```python
data = ind.leeTable(path_to_csv_file)
```

3. Create the blocks to be labeled

```python
blocks = dat.separaBloques(data, block_size, start_date) #For non-overlapping blocks
blocks = dat.bloquesDeslizantes(datos, block_size, window_size, start_date) #For overlapping blocks
```
where

* ```block_size``` is an integer that specifies the size of each block.

* ```start_date``` is a string with the format 'YYYY-MM-DD' that indicates the starting date.

* ```window_size``` is an integer that specifies the window size for overlapping blocks.

4. Start the labeling process (this might take a while so go and grab a cup of coffee :-p )

```python
lab_blocks = dat.etiquetaBloques(blocks,numGen ,popSize , flagOper, clean, execPrice, execStep)
```
where

* ```numGen``` is an integer that specifies the number of generations (suggestion: 30).

* ```popSize``` is an integer that specifies the population size (suggestion: 50).

* ```flagOper``` is a boolean that specifies if the number of transactions should be considered (suggestion: True).

* ```clean``` is a boolean that specifies if all the transactions causing a loss should be removed (suggestion: I STRONGLY ADVISE YOU TO SET THIS TO True).

* ```execPrice``` is a string that specifies the execution price that should be used, options are:
    - 'open': Open price.
    - 'mid': Mid price.
    - 'adj.close': Adjusted closed price (this is the suggested parameter).
    - 'close': Close price.

* ```h``` is an integer indicating the time in the future, after receiving the signal, that the execution price is going to be calculated. For example if the signal is received at time $t$ and $h = 1$, then the execution price is calculated with the prices from $t + h = t + 1$ (suggestion h = 1).

This function will show some messages of the progress of the EDA algorithm

```
Fin de la generacion 0 #Displays the end of the current generation
Mejor fitness hasta el momento -0.493349 #Displays the best fitness so far
```
