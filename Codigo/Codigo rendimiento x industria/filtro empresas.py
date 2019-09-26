import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from collections import defaultdict

rend =  pd.read_csv("csv_rendmientos.csv", sep=",")
rend = rend[["ticket", "rendimiento"]]
empresas_df =  pd.read_csv("constituents_csv.csv", sep=",")
empresas_df["Symbol"] = empresas_df["Symbol"].str.lower()
del empresas_df["Name"]
empresas_df = empresas_df[["Symbol", "Sector"]]
# empresas_df2=empresas_df["Symbol", "Sector"]

industrias= []
for index, row in empresas_df.iterrows():

    if row["Sector"] not in industrias:
        industrias.append(row["Sector"])



rend_x_empresa=[]
for index, row in rend.iterrows():
    tk = row["ticket"][:-3]
    rend_x_empresa.append([tk, row["rendimiento"]])

dic_final = {"industria":[],"rendimiento":[]}
ind_dic={}
ind_listas= []
for index, row in empresas_df.iterrows():
    empresa = row["Symbol"]

    industria = row["Sector"]

    if industria not in ind_dic:
        ind_listas.append(industria)


        ind_dic[industria]=[0, 1]

    for index, row in rend.iterrows():
        empresa_rend = row["ticket"][:-3]


        rendimiento = row["rendimiento"]
        if empresa == empresa_rend:
            cont=ind_dic[industria][1]
            cont+=1
            rendi=ind_dic[industria][0]
            rendi= rendi+rendimiento
            ind_dic[industria]=[rendi, cont]

for item in ind_dic:

    dic_final["industria"].append(item)
    dic_final["rendimiento"].append(float(ind_dic[item][0])/float(ind_dic[item][1]))

rend_x_industria = pd.DataFrame(dic_final)
rend_x_industria = rend_x_industria.sort_values(by="rendimiento", ascending=False)
rend_x_industria.to_csv (r'C:\Users\Nicolas Casassas\Desktop\Universidad\U 2019-2\Capstones\capstone\Codigo\rend_x_indus.csv', index = None, header=True)
