import numpy as np
import cmath 

#função carga
def Carga (Z):
    A = 1
    B = Z
    C = 0
    D = 1

    matriz = np.array(
        [
            [A,B],
            [C,D]
        ]
    )

    return matriz

#matriz carga derivada
def CargaDerivada(Z):
    A = 1
    B = 0
    C = 1/Z
    D = 1

    matriz = np.array(
        [
            [A,B],
            [C,D]
        ]
    )

    return matriz 
