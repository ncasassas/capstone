import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from collections import defaultdict


def archivo_no_vacio(fpath):
    return True if os.path.isfile(fpath) and os.path.getsize(fpath) > 0 else False



empresas_df =  pd.read_csv("constituents_csv.csv", sep=",")
empresas_df["Symbol"] = empresas_df["Symbol"].str.lower()
lista_sectores = list(empresas_df["Sector"])
dic_empresas_industria = defaultdict()
for index, accion in enumerate(empresas_df["Symbol"]):
    dic_empresas_industria[accion] = lista_sectores[index]

# filtro de fechas y filtro de empresas grandes#
data_unico = []
list_files = os.listdir("Stocks1/")
for csv in list_files:
    path = f"Stocks1/{csv}"
    index = csv.find(".us")
    simple = csv[0:index]
    if simple not in list(empresas_df["Symbol"]):
        continue
    # recorremos los archivos no vacios
    if archivo_no_vacio(path):
        df = pd.read_csv(path, sep=",")
        df = df[['Date', 'Open', 'Close', 'Volume']]
        df['ticker'] = csv.replace('.csv', '')
        df['Rendimiento'] = (df['Close'] - df['Open']) / df['Open']
        # filtramos para obtener los datos de hasta el 31 Dic de 2014
        df = df[(df['Date'] < '2015-01-01 00:00:00')]

        # filtramos por presencia bursatil
        if len(df.index)/ 1258 < 0.999:      # permitimos 1 dia de no presencia, 1258 es el maximo de presencias
            continue   # no la consideramos
        # si tiene suficiente presencia bursatil la consideramos
        data_unico.append(df)
data_unico = pd.concat(data_unico, ignore_index=True)
data_unico.reset_index(inplace=True, drop=True)
data_unico2 = data_unico[["ticker","Rendimiento"]] #data con solo el rendimiento y ticket

emp_dic={}

for index, row in data_unico2.iterrows():

    actual = row["ticker"]

    rend= row["Rendimiento"]
    if actual not in emp_dic:
        cont=1
        r_tot=rend
        emp_dic[actual]=[rend, cont]
    elif actual in emp_dic:
        cont+=1
        r_tot = r_tot+rend
        emp_dic[actual]=[r_tot, cont]
dic_final = {"ticket":[],"rendimiento":[]}
for item in emp_dic:
    dic_final["ticket"].append(item)
    dic_final["rendimiento"].append(emp_dic[item][0]/emp_dic[item][1])
    # dic_final[item]=emp_dic[item][0]/emp_dic[item][1]

print(dic_final)
csv_rendmientos = pd.DataFrame(dic_final)
csv_rendmientos.to_csv (r'C:\Users\Nicolas Casassas\Desktop\Universidad\U 2019-2\Capstones\capstone\Codigo\csv_rendmientos.csv', index = None, header=True)

# prueba=data_unico2.loc[[" a.us"]]
# print(prueba)
# empresas_df =  pd.read_csv("constituents_csv.csv", sep=",")
# empresas_df["Symbol"] = empresas_df["Symbol"].str.lower()
# empresas_df2=empresas_df[["Symbol", "Sector"]].copy
#
# print(empresas_df2)
