import numpy as np

# Defina sua matriz
matriz = np.array([[1, 2],
                   [3, 4]])

# Calcule a matriz inversa
matriz_inversa = np.linalg.inv(matriz)

print("Matriz original:")
print(matriz)

print("\nMatriz inversa:")
print(matriz_inversa)