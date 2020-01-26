# Procedure to create the training sets.

**This is run in an interactive python shell**.
**This should be executed after labeling the data (see README_LABELING)**.

1. Import the following modules

```python
import json
import datasets as dat
import indicadores as ind
```

2. Read the data from the csv of Yahoo Finance

```python
data = ind.leeTabla(path_to_csv_file)
```

3. Read the json file with the dictionary used in order to calculate the technical indicators (features).

```python
f = open(path_to_json_file)
dicc = json.load(f)
f.close()
```

4. Use the function ```dat.creaEntrenamiento``` in order to create the training datasets

```python
dat.creaEntrenamiento(data, dicc, arch_eti, ruta_eti, ruta_dest, activo)
```
where:

* ```data``` is a pandas dataframe with data of Yahoo Finance CSV file.

* ```dicc``` is a dictionary.

* ```arch_eti``` is a string that specifies the path of the CSV file containing the name of each labeled dataset.

* ```ruta_eti``` is a string that specifies the path to the folder that contains the labeled datasets.

* ```ruta_dest```is a string that specifies the path to the folder where all the training datasets are going to be stored.

* ```activo``` is an auxiliary string that is used as a prefix for the name of each training dataset.
