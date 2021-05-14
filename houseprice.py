# -*- coding: utf-8 -*-
"""
Ejercicio House Price

Guillermo Adam Merino

MDA

"""

import os  #importamos sistema operativo para gestionar directorios
import pandas as pd #importamos panda con el nick pd
import numpy as np #importamos numpy para operaciones sobre vectores y matrices
import matplotlib.pyplot as plt #importamos matplotlib para plots
import datetime as dt
import seaborn as sn
from pandas.api.types import CategoricalDtype #For definition of custom categorical data types (ordinal if necesary)
import scipy.stats as stats  # For statistical inference 


#%% Ingesta de datos

os.chdir(r'C:\Users\guill\Desktop\master\ejercicio_house_price\tarea_house_price')

houseprices = pd.read_csv(r'C:\Users\guill\Desktop\master\ejercicio_house_price\tarea_house_price\resources\houseprice.csv')



#%% Exploración gráfica del objetivo (precio de la vivienda).







