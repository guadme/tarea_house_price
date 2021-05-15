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

houseprices = pd.read_csv(r'C:\Users\guill\Desktop\master\ejercicio_house_price\tarea_house_price\resources\houseprice.csv', sep=';',
                          decimal=",")


#%% Exploración general

houseprices.info #informacion general del dataset
houseprices.dtypes  #tipo de dato de cada columna
houseprices.head(10) #head
houseprices.tail(10) #tail
houseprices.shape #nº filas y columnas
houseprices.columns #nombre de las columnas
pd.set_option("max_rows", 90) #poder visualizar todas las columnas en consola
pd.isnull(houseprices).sum() #numero de valores null por columna

#%% Exploración gráfica del objetivo (precio de la vivienda).

#Histograma precio

houseprices.SalePrice.describe()

M = houseprices.SalePrice.mean()
S=houseprices.SalePrice.std()
c1=M-S
c2=M+S
x=houseprices.SalePrice


plt.hist(x, edgecolor="Black")
plt.ylabel("Frecuency")
plt.xlabel("Price")
plt.title("Figure 1. Price Histogram")

plt.axvline(x=M,
            linewidth=1,
            linestyle="solid",
            Color="red",
            label="Mean")

plt.axvline(x=c1,
            linewidth=1,
            linestyle="dashed",
            Color="green",
            label="- SD")

plt.axvline(x=c2,
            linewidth=1,
            linestyle="dashed",
            Color="green",
            label="+ SD")

count = houseprices.SalePrice.count()

text= ('Count = ' + str(count))

props=dict(boxstyle="round", facecolor="white", lw=0.5)
plt.text(0,760,text, bbox=props)
plt. legend(loc='upper left', bbox_to_anchor=(0.73, 0.98))
plt.show()

#%%

# Media precio por año

grouped_date = houseprices.groupby('YrSold')
grouped_date_mean = grouped_date.SalePrice.mean()
grouped_date_mean = grouped_date_mean.to_frame()
grouped_date_mean.reset_index(inplace=True)

x2 = grouped_date_mean.YrSold
y2 = grouped_date_mean.SalePrice

c2006 = houseprices.loc[houseprices['YrSold'] == 2006].SalePrice.count()
c2007 = houseprices.loc[houseprices['YrSold'] == 2007].SalePrice.count()
c2008 = houseprices.loc[houseprices['YrSold'] == 2008].SalePrice.count()
c2009 = houseprices.loc[houseprices['YrSold'] == 2009].SalePrice.count()
c2010 = houseprices.loc[houseprices['YrSold'] == 2010].SalePrice.count()

text2 = ' Count 2006 = {} \n Count 2007 = {} \n Count 2008 = {} \n Count 2009 = {} \n Count 2006 = {}'.format(c2006,c2007,c2008,c2009,c2010)


#plt.figure(figsize = (5,5))
plt.scatter(x2,y2,s=50)
plt.plot(x2,y2)
plt.xticks(np.arange(2006, 2011, step=1), fontsize=15)
plt.title("Figure 2. Mean price x year")
plt.xlabel("Year")
plt.ylabel("Mean Price")

props2=dict(boxstyle="round", facecolor="white", lw=0.5)
plt.text(2008.7,1.642e9,text2, bbox=props2)
#plt. legend(loc='upper left', bbox_to_anchor=(0.73, 0.98))

plt.show()


#%%

#Correlacion con las variables numericas

price_corr = houseprices.corr().iloc[:,1]
price_corr = price_corr.to_frame()
price_corr.reset_index(inplace=True)

price_corr = price_corr.drop([1],axis=0)

plt.bar(price_corr['index'],price_corr['SalePrice'])
plt.xticks(rotation=90, fontsize=8)


#%% 

#2. Identificar valores faltantes: crear variables binarias y obtener un gráfico respecto de la variable objetivo.

#obtenemos numero de valores faltantes por columna

houseprices_nan_cols = ((pd.isnull(houseprices).sum()).to_frame()).reset_index()

houseprices_nan_cols = houseprices_nan_cols.rename(columns={'index' : 'variable', 0 : 'nan_number'})

#eliminamos de houseprices_nan_cols las columnas que no tienen nan


houseprices_nan_cols = houseprices_nan_cols.drop(houseprices_nan_cols[houseprices_nan_cols['nan_number']==0].index)


#Para las columnas numericas:
    
    # Vemos que hay columnas NUMERICAS con muchos valores perdidos,
    # se van a seguir los siguientes métodos dependiendo
    # la cantidad de valores nan:
    
        # - Más del 75% columna nan -> Eliminar columna: No aporta la suficiente info.
        # - Menos del 5% columna nan -> Se eliminan los registros
        # - El resto -> Media de la columna
    

#Creamos tres columnas: Over_75, Under_5, Other:
    
    #Over_75: True si el numero de nan es mayor al 75% del total
    ##Under_5: True si el numero de nan es mmenor al 5% del total
    #Other: Other


houseprices_nan_cols['over_75'] = [True if s > ((houseprices['Id'].count())*0.75) else False for s in houseprices_nan_cols['nan_number']]

houseprices_nan_cols['Under_5'] = [True if s < ((houseprices['Id'].count())*0.05) else False for s in houseprices_nan_cols['nan_number']]

houseprices_nan_cols['other'] = [True if ((s < ((houseprices['Id'].count())*0.75)) & (s > ((houseprices['Id'].count())*0.05))) else False for s in houseprices_nan_cols['nan_number']] 


#Obtenemos las columnas a eliminar

del_col = ((houseprices_nan_cols[houseprices_nan_cols['over_75'] == True]).variable).to_list()

#obtenemos columnas para eliminar registros

del_row = ((houseprices_nan_cols[houseprices_nan_cols['Under_5'] == True]).variable).to_list()

#columnas para hacer la media

mean_col = ((houseprices_nan_cols[houseprices_nan_cols['other'] == True]).variable).to_list()

houseprices_test = houseprices

#Ahora aplicamos los cambios al dataset

houseprices = houseprices.drop(columns=del_col)

mean_col_num = ((houseprices[mean_col].select_dtypes(exclude='object')).columns).to_list()

[houseprices[col].fillna(houseprices[col].mean(), inplace=True) for col in mean_col_num]

pd.isnull(houseprices).sum()

#Para el resto de variables categóricas eliminaremos la columna FireplaceQu

houseprices.drop(['FireplaceQu'], axis = 1, inplace=True)


#utilizamos dropna para el resto de las categoricas

houseprices = houseprices.dropna()

pd.isnull(houseprices).sum()

#%%



# 3. Outliers

#Como hemos visto en el primer apartado


M = houseprices.SalePrice.mean()
S=houseprices.SalePrice.std()
c1=M-S
c2=M+S
x=houseprices.SalePrice


plt.hist(x, edgecolor="Black")
plt.ylabel("Frecuency")
plt.xlabel("Price")
plt.title("Figure 1. Price Histogram")

plt.axvline(x=M,
            linewidth=1,
            linestyle="solid",
            Color="red",
            label="Mean")

plt.axvline(x=c1,
            linewidth=1,
            linestyle="dashed",
            Color="green",
            label="- SD")

plt.axvline(x=c2,
            linewidth=1,
            linestyle="dashed",
            Color="green",
            label="+ SD")

count = houseprices.SalePrice.count()

text= ('Count = ' + str(count))

props=dict(boxstyle="round", facecolor="white", lw=0.5)
plt.text(0,760,text, bbox=props)
plt. legend(loc='upper left', bbox_to_anchor=(0.73, 0.98))
plt.show()


#vemos ciertos outliers en 0

#elimino los datos con valores de precio = 0 y vuelvo a hacer la grafica



houseprices = houseprices.drop(houseprices[houseprices['SalePrice']<0.25e9].index)


#%%

houseprices_out = houseprices

M = houseprices_out.SalePrice.mean()
S=houseprices_out.SalePrice.std()
c1=M-S
c2=M+S
x=houseprices_out.SalePrice


plt.hist(x, edgecolor="Black")
plt.ylabel("Frecuency")
plt.xlabel("Price")
plt.title("Figure 1. Price Histogram")

plt.axvline(x=M,
            linewidth=1,
            linestyle="solid",
            Color="red",
            label="Mean")

plt.axvline(x=c1,
            linewidth=1,
            linestyle="dashed",
            Color="green",
            label="- SD")

plt.axvline(x=c2,
            linewidth=1,
            linestyle="dashed",
            Color="green",
            label="+ SD")

count = houseprices_out.SalePrice.count()

text= ('Count = ' + str(count))

props=dict(boxstyle="round", facecolor="white", lw=0.5)
plt.text(2.4e9,300,text, bbox=props)
plt. legend(loc='upper left', bbox_to_anchor=(0.73, 0.98))
plt.show()



#%%