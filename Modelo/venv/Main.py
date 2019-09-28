from Funciones_Modelos import modelo_por_industria, modelo_entre_industrias
import json
import time


def modelacion(lb_por_industria, ub_por_industria, ret_min_por_industria,
               lb_entre_industrias, ub_entre_industrias, ret_min_entre_industrias):

    industrias = ['Basic Materials',
                  'Communication Services',
                  'Consumer Cyclical',
                  'Consumer Defensive',
                  'Energy',
                  'Financial Services',
                  'Healthcare',
                  'Industrials',
                  'Real Estate',
                  'Technology',
                  'Utilities']

    d = {}
    for industria in industrias:
        m =  modelo_por_industria(industria, lb_por_industria,
                                  ub_por_industria, ret_min_por_industria)
        d.update(m)

    m = modelo_entre_industrias(lb_entre_industrias, ub_entre_industrias,
                                ret_min_entre_industrias)

    total = {}
    for sector in m:
        ponderador = m[sector]
        for accion in d[sector]:
            valor = d[sector][accion] * ponderador
            total[accion] = valor

    params = {'parametros': [lb_por_industria,
                             ub_por_industria,
                             ret_min_por_industria,
                             lb_entre_industrias,
                             ub_entre_industrias,
                             ret_min_entre_industrias]}
    total.update(params)

    return total

'''
Parámetros
'''
lb_por_industria = 0.03
ub_por_industria = 0.1
ret_min_por_industria = 0.001
lb_entre_industrias = 0.05
ub_entre_industrias = 0.25
ret_min_entre_industrias = 0.001

inicio = time.time()

m = modelacion(lb_por_industria, ub_por_industria, ret_min_por_industria,
               lb_entre_industrias, ub_entre_industrias, ret_min_entre_industrias)

final = time.time()

with open(f'Resultados acciones.json', 'w') as file:
    dicto = json.dumps(m)
    file.write(dicto)

tiempo = final - inicio
print(f'El modelo demoró {tiempo:.2f} segundos en correr.')