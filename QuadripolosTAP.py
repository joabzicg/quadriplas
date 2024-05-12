import numpy as np #importando as bibliotecas necessárias para o projeto
import cmath

#DISTÂNCIA DAS LINHAS DE TRANSMISSÃO EM KM
dLT1_2_3 = 80
dLT4_5 = 100
dLT6 = 90

#PARÂMETROS DO TRANSFORMADOR T = [V1,V2,Rm,Xm]
T1_p = [69000, 226874.12,4320,5050]
T2_p= [230000,138000,432000,505000]
T3_p = [138000,69000,402000,607000]

#IMPEDÂNCIA SÉRIE DE THÉVENIN
Zf = 4 + 1j*0.38 #impedância

w = 2*np.pi*60 #frequência angular em rad/s

#CARGAS EM DERIVAÇÃO
Zc1 = 7900 + 1j*w*41
Zc2= 1375.55 + 1j*w*7.05
Zc3 = 620 + 1j*w*3.4

#paramêtros da LINHA '1_2_3', '4_5' e 6 [R, L, C]:
LT1_LT2_LT3 = [dLT1_2_3*0.172,dLT1_2_3*2.18e-3,dLT1_2_3*0.0136e-6]
LT4_LT5 = [dLT4_5*0.172,dLT4_5*2.18e-3,dLT4_5*0.0136e-6]
LT6_ = [dLT6*0.172,dLT6*2.18e-3,dLT6*0.0136e-6]

#MATRIZES LINHA DE TRANSMISSÃO
def M_Linha(Linha):
    #Admitância Y da linha (Y1=Y2)
    Y = 1/(1/(1j*w*(Linha[2]/2)))
    #Impedância Z da linha
    Z = Linha[0]+(1j*w*Linha[1])
    #Calculando matriz ABCD

    A = 1+(Y*Z)
    B = Z
    C = (2*Y)+(Y*Y*Z)
    D = 1+(Y*Z)
    
    matrizLinha = np.array(
        [
            [A,B],
            [C,D]
        ]
    )
    return matrizLinha
    
#Função carga em série
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

#Função carga em derivação
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

#Função de definição da matriz transmissão do transformador
def Transformador(Transfp): 
    Z1 = 7.6e-3 + 1j*3.8e-3 #Indicando as impedâncias Z1 e Z2 do circuito equivalente do transformador
    Z2 = 33.9e-3 + 1j*0.85e-3
    
    V1 = Transfp[0] #Recebendo os valores de entrada
    V2 = Transfp[1] 
    Rm = Transfp[2] 
    Xm = Transfp[3] 

    Y = (Rm + 1j*Xm)/(Rm*1j*Xm) #Indicando a admitância Y do circuito equivalente do transformador

    N = V1/V2 #Relação V1/V2

    A = N*(1 + (Y*Z1)) #Construção da Matriz de transmissão
    B = (Z1 + Z2 + Y*Z1*Z2)/N
    C = N*Y
    D = (1 + Y*Z2)/N

    matriz = np.array(
        [
            [A,B],
            [C,D]
        ]
    )
    return matriz

#FUNÇÃO PARA REALIZAR MULTIPLICAÇÃO DE MATRIZES
def Associar_Matriz_em_Cascata (matriz1, matriz2):
    bloco =  np.dot(matriz1, matriz2)
    
    return bloco

#FUNÇÃO PARA REALIZAR ASSOCIAÇÃO PARALELO DE MATRIZES TRANSMISSÃO
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

#CRIANDO OBJETOS DOS COMPONENTES DA LINHA
Zth = Carga(Zf) #Impedância série do começo da linha
T1 = Transformador(T1_p) #Primeiro Transformador
T2 = Transformador(T2_p) #Segundo Transformador
T3 = Transformador(T3_p) #Terceiro Transformador
LT1 = M_Linha(LT1_LT2_LT3) #Primeira Linha
LT2 = M_Linha(LT1_LT2_LT3) #Segunda Linha
LT3 = M_Linha(LT1_LT2_LT3) #Terceira Linha
LT4 = M_Linha(LT4_LT5) #Quarta Linha
LT5 = M_Linha(LT4_LT5) #Quinta Linha
LT6 = M_Linha(LT6_) #Sexta Linha
Z1 = CargaDerivada(Zc1) #Cargas 1, 2 e 3
Z2 = CargaDerivada(Zc2)
Z3 = CargaDerivada(Zc3)

#CRIANDO BLOCOS DA LINHAS POR ASSOCIAÇÃO DE MATRIZES
matriz1 = Associar_Matriz_em_Cascata (Zth,T1)
paralel_LT1_2 = Matriz_Paralelo (LT1,LT2)
paralel_LT1_2_3 = Matriz_Paralelo (paralel_LT1_2,LT3)
matriz2 = Associar_Matriz_em_Cascata (matriz1, paralel_LT1_2_3) #Matriz Transmissão até a carga 1
matriz3 = Associar_Matriz_em_Cascata (matriz2, Z1)
matriz4 = Associar_Matriz_em_Cascata (matriz3, Matriz_Paralelo (LT4 ,LT5))
matriz5 = Associar_Matriz_em_Cascata (matriz4, T2) #Matriz Transmissão até a carga 2
matriz6 = Associar_Matriz_em_Cascata (matriz5, Z2)
matriz7 = Associar_Matriz_em_Cascata (matriz6, LT6)
matriz8 = Associar_Matriz_em_Cascata (matriz7, T3) #Matriz Transmissão até a carga 3
Fim_daL_Linha = Associar_Matriz_em_Cascata (matriz8, Z3)

#CALCULANDO TENSÃO E CORRENTE NAS CARGAS
#Encontrando Vc e IC em Z3
print("o=> Tensão e corrente em rms na carga Z3:")
Vg = 69e+3 #tensão na entrada do quadripolo
Vc = (Vg*Zc3)/(matriz8[0][0]*Zc3 + matriz8[0][1]) #Tensão na carga 3 
Ic = Vc/Zc3 #Corrente na carga 3

#Forma retangular dos fasores
print("No formato retangular-----------------")
print (f"Vcarga3 = {Vc:.2f} V") #imprimindo na tela
print (f"Icarga3 = {Ic:.2f} A")

#Forma polar dos fasores
print("No formato polar----------------------")
absVc, angVc = cmath.polar(Vc)
absIc, angIc = cmath.polar(Ic)
angVc = np.rad2deg(angVc)
angIc = np.rad2deg(angIc)
print(f"Vcarga3 = {absVc:.2f} ∠ {angVc:.2f}° V")
print(f"Icarga3 = {absIc:.2f} ∠ {angIc:.2f}° A\n")

#Encontrando Vc e IC em Z1
print("o=> Tensão e corrente em rms na carga Z1:")
Vg = 69e+3
Vc = (Vg*Zc1)/(matriz2[0][0]*Zc1 + matriz2[0][1])
Ic = Vc/ Zc1

#Forma retangular dos fasores
print("No formato retangular-----------------")
print(f"Vcarga1 = {Vc:.2f} V")
print(f"Icarga1 + {Ic:.2f} A")

#Forma polar dos fasores
print("No formato polar----------------------")
absVc, angVc = cmath.polar(Vc)
absIc, angIc = cmath.polar(Ic)
angVc = np.rad2deg(angVc)
angIc = np.rad2deg(angIc)
print(f"Vcarga1 = {absVc:.2f} ∠ {angVc:.2f}° V")
print(f"Icarga1 = {absIc:.2f} ∠ {angIc:.2f}° A\n")

#Encontrando Vc e IC em Z2
print("o=> Tensão e corrente em rms na carga Z2")
Vg = 69e+3
Vc = (Vg*Zc2)/(matriz5[0][0]*Zc2 + matriz5[0][1])
Ic = Vc/Zc2

#Forma retangular dos fasores
print("No formato retangular-----------------")
print(f"Vcarga2 = {Vc:.2f} V")
print(f"Icarga2 = {Ic:.2f} A")

#Forma polar dos fasores
print("No formato polar----------------------")
absVc, angVc = cmath.polar(Vc)
absIc, angIc = cmath.polar(Ic)
angVc = np.rad2deg(angVc)
angIc = np.rad2deg(angIc)
print(f"Vcarga2 = {absVc:.2f} ∠ {angVc:.2f}° V")
print(f"Icarga2 = {absIc:.2f} ∠ {angIc:.2f}° A")
