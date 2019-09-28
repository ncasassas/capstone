from Funciones_Modelos import modelo_por_industria, modelo_entre_industrias
import json

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

def modelacion(lb_por_industria, ub_por_industria, ret_min_por_industria,
               lb_entre_industrias, ub_entre_industrias, ret_min_entre_industrias):

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

    return total

m = modelacion(0.03, 0.1, 0.001, 0.05, 0.25, 0.001)

ret = {'parametros': [0.03, 0.1, 0.001, 0.05, 0.25, 0.001]}
m.update(ret)

with open(f'Resultados acciones.json', 'w') as file:
    dicto = json.dumps(m)
    file.write(dicto)