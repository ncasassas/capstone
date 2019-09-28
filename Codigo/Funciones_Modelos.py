from gurobipy import *
from Excel import csv_generator, covs_matrix
from Json import dict_rendimientos

'''
Retorna un diccionario: { Industria: {w_(Ticker1): %, w_(Ticker2): %, ...} }
'''
def modelo_por_industria(industria, lower_bound, upper_bound, ret_min):

    #print(f'industria: {industria}')

    path_covs = f'matrices_cov_por_sector/{industria}_cov.csv'
    path_json = f'rendimientos_promedio_sectoriales/acciones_{industria}.json'

    generator = csv_generator(path_covs)
    Q, names = covs_matrix(generator)
    numbers_to_names = {number: names[number] for number in range(len(names))}

    R = dict_rendimientos(path_json)

    N = len(R)

    model = Model()

    w = {}
    z = {}
    for j in range(N):
        w[j] = model.addVar(lb=0, ub=upper_bound,
                            name=f'{numbers_to_names[j]}')
        z[j] = model.addVar(vtype=GRB.BINARY, name=f'{numbers_to_names[j]}')

    model.addConstr(quicksum(w[j] * R[numbers_to_names[j]]
                             for j in range(N)) >= ret_min, name='R1')

    model.addConstr(quicksum(w[j] for j in range(N)) == 1, name='R2')

    for j in range(N):
        model.addConstr(w[j] >= lower_bound * z[j], name=f'R3.1_({j})')
        model.addConstr(w[j] <= z[j], name=f'R3.2_({j})')

    obj = quicksum(Q[i, j] * w[i] * w[j] for i in range(N) for j in range(N))
    model.setObjective(0.5 * obj, sense=GRB.MINIMIZE)

    model.update()
    model.Params.OutputFlag = 0

    model.optimize()

    if model.status == GRB.Status.INF_OR_UNBD:
        print('Modelo es infactible o no acotado.')
        exit(0)

    else:
        vars = {w[j].VarName: w[j].X for j in range(N) if z[j].X}

    return {industria: vars}


'''
Retorna un diccionario: {W_(Industria): %}
'''
def modelo_entre_industrias(lower_bound, upper_bound, ret_min):

    path_covs = f'matriz_cov_entre_sectores/matriz_cov_sectores.csv'
    path_json = f'rendimientos_por_sector/rendimientos_promedio_por_sector.json'

    generator = csv_generator(path_covs)
    Q, names = covs_matrix(generator)
    numbers_to_names = {number: names[number] for number in range(len(names))}

    R = dict_rendimientos(path_json)

    N = len(R)

    model = Model()

    w = {}
    z = {}
    for j in range(N):
        w[j] = model.addVar(lb=0, ub=upper_bound,
                            name=f'{numbers_to_names[j]}')
        z[j] = model.addVar(vtype=GRB.BINARY, name=f'{numbers_to_names[j]}')

    model.addConstr(quicksum(w[j] * R[numbers_to_names[j]]
                             for j in range(N)) >= ret_min, name='R1')

    model.addConstr(quicksum(w[j] for j in range(N)) == 1, name='R2')

    for j in range(N):
        model.addConstr(w[j] >= lower_bound * z[j], name=f'R3.1_({j})')
        model.addConstr(w[j] <= z[j], name=f'R3.2_({j})')

    obj = quicksum(Q[i, j] * w[i] * w[j] for i in range(N) for j in range(N))
    model.setObjective(0.5 * obj, sense=GRB.MINIMIZE)

    model.update()
    model.Params.OutputFlag = 0

    model.optimize()

    if model.status == GRB.Status.INF_OR_UNBD:
        print('Modelo es infactible o no acotado.')
        exit(0)

    else:
        vars = {w[j].VarName: w[j].X for j in range(N) if z[j].X}

    return vars

"""
m1 = modelo_por_industria('Healthcare', 0.01, 1, 0.001)
i = 0
for c in m1['Healthcare']:
    i += 1
    print(f'{c}: {m1["Healthcare"][c]}')
print(f'\nNúmero de acciones en las que invertir: {i}')

print()

m2 = modelo_entre_industrias(0.01, 1, 0.001)
j = 0
for c in m2:
    j += 1
    print(f'{c}: {m2[c]}')
print(f'\nNúmero de industrias en las que invertir: {j}')
"""
