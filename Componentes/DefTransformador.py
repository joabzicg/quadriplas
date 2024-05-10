import numpy as np
import cmath

def Transformador(Transfp): #Função de definição da matriz transmissão do transformador
    Z1 = 7.6e-3 + 1j*3.8e-3 #Indicando as impedâncias Z1 e Z2 do circuito equivalente do transformador
    Z2 = 33.9e-3 + 1j*0.85e-3
    
    V1 = Transfp[0] #Recebendo os valores de entrada
    V2 = Transfp[1] 
    Rm = Transfp[2] 
    Xm = Transfp[3] 

    Y = (Rm + 1j*Xm)/(Rm*1j*Xm) #Indicando a admitância Y do circuito equivalente do transformador

    N = V1/V2 #Relação V1/V2

    A = (1/N)+(Y*Z1) #Construção da Matriz de transmissão
    B = N*(Z1 + Z2 + (Y*Z1*Z2))
    C = (1/N)*Y
    D = N*(1+(Y*Z2))

    matriz = np.array(
        [
            [A,B],
            [C,D]
        ]
    )
    return matriz
