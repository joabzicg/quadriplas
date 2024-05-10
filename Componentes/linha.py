import numpy as np
import cmath

#Frequência angular
w = 2*np.pi*60 

#MATRIZES LINHA DE TRANSMISSÃO
def M_Linha(Linha):
    #Admitância Y da linha (Y1=Y2)
    Y = 1/(1/1j*w*(Linha[2]/2))

    #Impedância Z da linha
    Z = Linha[0]+(1j*w*Linha[1])
    #Calculando matriz ABCD

    A = 1+Y*Z
    B = Z
    C = (2*Y+Y*Y*Z)
    D = 1+Y*Z
    
    matrizLinha = np.array(
        [
            [A,B],
            [C,D]
        ]
    )
    return matrizLinha
