from gurobipy import *
from Excel import csv_generator, covs_matrix
from Json import dict_rendimientos

'''
Modelo de Markowitz por Industrias - Capstone Investigación Operativa
'''

'''
Seteamos nuestros parámetros.
'''
lower_bound = 0.03
upper_bound = 1
ret_min = 0.001

'''
Creamos los paths a los archivos deseados.
'''

path_covs = f'matriz_cov_entre_sectores/matriz_cov_sectores.csv'
path_json = f'rendimientos_por_sector/rendimientos_promedio_por_sector.json'

'''
Cargamos los retornos esperados de cada acción en un diccionario.
'''

R = dict_rendimientos(path_json)

'''
Cargamos la matriz de covarianzas, representada por un diccionario.
'''

generator = csv_generator(path_covs)
Q, names = covs_matrix(generator)
numbers_to_names = {number: names[number] for number in range(len(names))}

'''
Representamos la cantidad de variables por N.
'''
N = len(R)

'''
Declaramos el modelo.
'''
model = Model()

'''
Creamos diccionarios de variables. Las w corresponden a la fracción del
prespuesto destinado a cada acción. Las z corresponden a si se invierte o no
en cada acción.
'''
w = {}
z = {}
for j in range(N):
    w[j] = model.addVar(lb=0, ub=upper_bound, name=f'W_({numbers_to_names[j]})')
    z[j] = model.addVar(vtype=GRB.BINARY, name=f'Z_({numbers_to_names[j]})')

'''
Agregamos las restricciones, que corresponden a:
1.) El retorno esperado del portafolio debe tener un mínimo establecido.
2.) La suma de las fracciones del portafolio debe sumar 1.
3.) Si se invierte en una acción, se debe invertir por lo menos una fracción
    mínima del presupuesto.
'''
model.addConstr(quicksum(w[j] * R[numbers_to_names[j]]
                         for j in range(N)) >= ret_min, name='R1')

model.addConstr(quicksum(w[j] for j in range(N)) == 1, name='R2')

for j in range(N):
    model.addConstr(w[j] >= lower_bound * z[j], name=f'R3.1_({j})')
    model.addConstr(w[j] <= z[j], name=f'R3.2_({j})')

'''
Seteamos la función objetivo, que corresponde a (x^T)Qx, y queremos minimizarla.
'''
obj = quicksum(Q[i, j] * w[i] * w[j] for i in range(N) for j in range(N))
model.setObjective(0.5 * obj, sense=GRB.MINIMIZE)

'''
Actualizamos el modelo con todo lo que hemos hecho. Además, seteamos que no
entregue información innecesaria.
'''
model.update()
model.Params.OutputFlag = 0

'''
Finalmente, corremos el solver y mostramos los resultados.
'''
model.optimize()

if model.status == GRB.Status.INF_OR_UNBD:
    print('Modelo es infactible o no acotado.')
    exit(0)

else:
    print(f'Valor Objetivo: {model.objVal}\n')
    for j in w:
        if z[j].X:
            print(f'{w[j].VarName}: {w[j].X}')
