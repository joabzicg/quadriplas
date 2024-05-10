import numpy as np
def Matriz_Paralelo (matriz1, matriz2):
    Aa =  matriz1[0][0]
    Ba =  matriz1[0][1]
    Ca =  matriz1[1][0]
    Da =  matriz1[1][1]
    Ab =  matriz2[0][0]
    Bb =  matriz2[0][1]
    Cb =  matriz2[1][0]
    Db =  matriz2[1][1]

    A = (Aa*Bb + Ab*Ba)/(Ba + Bb)
    B = (Ba*Bb)/(Ba + Bb)
    C = Ca + Cb + ((Aa - Ab)*(Db - Da))/(Ba + Bb)
    D = (Bb*Da + Ba*Db)/(Ba + Bb)

    matriz = np.array(
        [
            [A,B],
            [C,D]
        ]
    )

    return matriz
