import numpy as np

#FUNÇÃO PARA REALIZAR MULTIPLICAÇÃO DE MATRIZES
def Matriz_Cascata (matriz1, matriz2):
    bloco =  np.dot(matriz1, matriz2)
    return bloco