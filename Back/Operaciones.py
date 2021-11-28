from random import seed
from random import randint
import numpy
# Genera una matriz de n * l de números complejos aleatorios
def genradorDeMatriz(n, l):
    matriz = []
    seed()
    for x in range (n):
        # se crean las columnas de una fila l y se guarda en n
        m = [(randint(-10,10)+ randint(-10,10)*1j) for i in range(l)]
        matriz.append(m)
    Mostrar("Matriz generada: ", matriz, 2)
    return matriz
# Devuelve el promedio de las magnitudes los elementos de una lista de matrices
def Promedio(h):
    hPromedio = numpy.zeros_like(h[0], dtype=float, order='K')
    # for i in range(len(h)):
    #     for j in range(len(h[i])):
    #         for k in range(len(h[i][j])):
    #             # hPromedio[j][k] += (h[i][j][k].conjugate()*h[i][j][k]).real
    #             hPromedio[j][k] += abs(h[i][j][k])*abs(h[i][j][k])
    
    for i in range(len(h)):
        tempAbs = numpy.abs(h[i])
        tempAbs = tempAbs*tempAbs
        hPromedio += tempAbs
    # for i in range(len(hPromedio)):
    #     for j in range(len(hPromedio[i])):
    #         hPromedio[i][j]/=len(h)
    hPromedio = hPromedio/len(h)
    return hPromedio
# Perfil de potecina de retardo    
def PPR(h):
    p = [0 for i in range(len(h[0]))]
    for i in range(len(h)):
        for j in range(len(h[i])):
            p[j]+=h[i][j]
    for i in range(len(p)):
        p[i]/=len(h)
    return p
# Calcula la transformada de fourier de una lista de números
def TDF(h):
    H = numpy.fft.fft(h)    # De naturaleza compleja
    return H
# Mostrar matrices
def Mostrar(texto, matriz, dimensions):
    if (texto):
        print(texto)
    if (dimensions == 2):
        for fila in matriz:
            for valor in fila:
                print(valor, end=" \t")
            print()
    elif (dimensions == 1):
        for fila in matriz:
            print(fila, end=" \t")
        print()
# Funcion de dispercion
def FDD(h):
    Ret = numpy.zeros_like(h[0], dtype=object, order='K')
    # for i in range(len(h)):
    #     for l in range(len(h[0][0])):
    #         temp = []
    #         for n in range(len(h[0])):
    #             temp.append(h[i][n][l])
    #         temp = numpy.fft.fft(temp)
    #         for n in range(len(h[0])):
    #             Ret[n][l] += abs(temp[n])*abs(temp[n])
    h2 = numpy.zeros( (len(h), len(h[0][0]), len(h[0])), dtype=numpy.complex128)
    Ret2 = numpy.zeros_like(h2[0], dtype=object, order='K')
    for i in range(len(h2)):
        h2[i] = h[i].T
        for j in range(len(h2[i])):
            h2[i][j] = numpy.fft.fft(h2[i][j], norm="ortho")
        tempAbs = numpy.abs(h2[i])
        tempAbs = tempAbs*tempAbs
        Ret2 += tempAbs
    Ret = Ret2.transpose()
    Ret = Ret/len(h)
    return Ret
# Densidad espectral de potencia
def DEDP(h): # h debe ser funcion de dispercion
    p = [0 for i in range(len(h))]
    for i in range(len(h)):
        for j in range(len(h[i])):
            p[i]+=h[i][j]
    for i in range(len(p)):
        p[i] = p[i] / len(h[0])
    return p
# Funcion de correlacion temporal
def FCT(h): #h debe ser la densidad espectral de potencia
    H = numpy.fft.ifft(h, norm="ortho").real
    return H
# Funcion de correlacion frecuencia
def FDA(h):
    H = numpy.fft.fft(h).real
    return H
def FillWith0s(lista, limite):
    listat = numpy.empty_like (lista)
    listat[:] = lista
    for i in range(len(lista), limite):
        listat = numpy.append(listat, 0)
    return listat
def innit():
    # Generar matrices con valores aleatorios #
    h = []
    for i in range(4):
        h.append(genradorDeMatriz(2, 3))
        #h.append(genradorDeMatriz(256, 32))
    print("realizaciones: ", len(h))
    print("n: ", len(h[0]))
    print("l: ", len(h[0][0]))

    # Almacenar el promedio de las magnitudes de las matrices
    P = Promedio(h)
    # Calcular el Perfil de potencia de retardo
    pdpr = PPR(P)
    # Calcular transformada de fourier, funcion de correlacion en frecuencia +2048 0, rellenar
    TransFourier = TDF(FillWith0s(pdpr, 2048))
    # Calcular la magnitud de cada elemento de la transformada de fourier
    Magnitude = [abs(TransFourier[i]) for i in range(len(TransFourier))]
    t1 = FDD(h)
    t2 = DEDP(t1)
    t3 = FCT(t2)

    
    #Mostrar("Promedio: ", P, 2)
    Mostrar("Perfil de potencia de retardo: ", pdpr, 1)
    Mostrar("Transformada de fourier: ", TransFourier, 1)
    Mostrar("Magnitud de cada elemento de la transformada de fourier:", Magnitude, 1)
    Mostrar("Funcion de dispersion:", t1, 2)
    Mostrar("Densidad espectral de potencia:", t2, 1)
    Mostrar("Funcion de correlacion temporal:", t3, 1)



def main():
    # Generar matrices con valores aleatorios #
    h = []
    for i in range(4):
        h.append(genradorDeMatriz(2, 3))
        #h.append(genradorDeMatriz(256, 32))
    print("realizaciones: ", len(h))
    print("n: ", len(h[0]))
    print("l: ", len(h[0][0]))

    # Almacenar el promedio de las magnitudes de las matrices
    #P = Promedio(h)
    # Calcular el Perfil de potencia de retardo
    #pdpr = PPR(P)
    # Calcular transformada de fourier, funcion de correlacion en frecuencia +2048 0, rellenar
    #TransFourier = TDF(FillWith0s(pdpr, 2048))
    # Calcular la magnitud de cada elemento de la transformada de fourier
    #Magnitude = [abs(TransFourier[i]) for i in range(len(TransFourier))]
    t1 = FDD(h)
    t2 = DEDP(t1)
    t3 = FCT(t2)

    Mostrar("Funcion de dispersion:", t1, 2)
    Mostrar("Densidad espectral de potencia:", t2, 1)
    Mostrar("Funcion de correlacion temporal:", t3, 1)
    # Mostrar("Promedio: ", P, 2)
    # Mostrar("Perfil de potencia de retardo: ", pdpr, 1)
    # Mostrar("Transformada de fourier: ", TransFourier, 1)
    # Mostrar("Magnitud de cada elemento de la transformada de fourier:", Magnitude, 1)



#main()
#innit()