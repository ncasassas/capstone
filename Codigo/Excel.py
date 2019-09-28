from collections import deque

def csv_generator(path):
    with open(path, 'r') as file:
        for row in file:
            yield row


def covs_matrix(generator):
    covs = {}
    i = -1
    for linea in generator:
        if i == -1:
            empresas = linea.strip().split(',')[1:]
        else:
            lista = linea.strip().split(',')[1:]
            for j in range(len(empresas)):
                covs[i, j] = float(lista[j])
        i += 1
    return covs, empresas


generator = csv_generator('matrices_cov_por_sector/Communication Services_cov.csv')
matrix, names = covs_matrix(generator)

'''
print(matrix)
print(names)
'''
