import matplotlib.pyplot as plt
import csv
from . import Operaciones as Op
import numpy as np
import time
import os
from datetime import datetime
import json
from tqdm import tqdm


class head:
    def __init__(self, pos, time):
        #self.time = datetime.today().strftime('%Y-%m-%d %H:%M:%f')
        self.time = time
        self.possition = pos
class sesion_header:
    def __init__(self, name, size, dir, pos):
        self.name = name
        self.size = size
        self.dir = dir
        self.coordenates = pos
class controller:

    def __init__(self, name):
        self.count = 0
        if name == '':
            self.date = datetime.today().strftime('%Y-%m-%d %H.%M')
        else:
            self.date = name
        self.dir = "./Saves/" + self.date + "/"
        self.positions = []
        print(self.date)

    def makeOp(self, h, coord, Gpstime):
        # Perfil de potencia de retardo
        startC = time.time()
        start = time.time()
        average = Op.Promedio(h)
        print('average time: ', time.time() - start)
        start = time.time()
        PDDR = Op.PPR(average)
        print('PDDR time:    ', time.time() - start)
        start = time.time()
        # Funcion de dispersion
        FDD = Op.FDD(h)
        print('FDD time:     ', time.time() - start)
        start = time.time()
        # Autocorrelación de frecuencia
        FDA = Op.FDA(Op.FillWith0s(PDDR, 2048))
        print('FDA time:     ', time.time() - start)
        start = time.time()
        # Densidad espectral de potencia
        DEDP = Op.DEDP(FDD)
        print('DEDP time:    ', time.time() - start)
        start = time.time()
        # Funcion de correlacion temporal
        FDCT = Op.FCT(DEDP)
        print('FDCT time:    ', time.time() - start)
        print('time of all operations: ', time.time() - startC)

        # Guardar los datos
        start = time.time()

        dir = self.dir + str(self.count)

        if not os.path.exists(dir):
            os.makedirs(dir)

        text_file = open(dir + "/header.json", "w")
        text_file.write(json.dumps(head(coord, Gpstime).__dict__))
        text_file.close()
        self.positions.append(coord)

        np.savetxt(dir + "/perfilDePotenciaDeRetardo.csv", [PDDR], fmt='% s', delimiter=',', newline='\n')
        np.savetxt(dir + "/funcionDeDispersion.csv", FDD, fmt='% s', delimiter=',', newline='\n')
        np.savetxt(dir + "/correlacionDeFrecuencia.csv", [FDA], fmt='% s', delimiter=',', newline='\n')
        np.savetxt(dir + "/densidadEspectralDePotencia.csv", [DEDP], fmt='% s', delimiter=',', newline='\n')
        np.savetxt(dir + "/correlacionTemporal.csv", [FDCT], fmt='% s', delimiter=',', newline='\n')
        self.count += 1
        print('time for saving the data in csv: ', time.time() - start)
        #self.showGraphs(PDDR, FDA, FDD, DEDP, FDCT)

    def close(self):
        print("Closing the sesion")

        text_file = open("./Saves/" + self.date + ".json", "w")
        text_file.write(json.dumps(sesion_header(self.date, self.count, "/"+self.date+"/", self.positions).__dict__))
        text_file.close()

        print("Making the average graphs...")

        print("Power Delay Profile:")
        PDDR = []
        for index in tqdm(range(self.count)):
            dir = self.dir + str(index)
            with open(dir + "/perfilDePotenciaDeRetardo.csv") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for x in csv_reader:
                    PDDR.append(np.array(x).astype(float))

        print("Frequency Autocorrelation:")
        FDA = []
        for index in tqdm(range(self.count)):
            dir = self.dir + str(index)
            with open(dir + "/correlacionDeFrecuencia.csv") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for x in csv_reader:
                    FDA.append(np.array(x).astype(float))

        print("Power Spectral Density:")
        DEDP = []
        for index in tqdm(range(self.count)):
            dir = self.dir + str(index)
            with open(dir + "/densidadEspectralDePotencia.csv") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for x in csv_reader:
                    DEDP.append(np.array(x).astype(float))

        print("Time Autocorrelation:")
        FDCT = []
        for index in tqdm(range(self.count)):
            dir = self.dir + str(index)
            with open(dir + "/correlacionTemporal.csv") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for x in csv_reader:
                    FDCT.append(np.array(x).astype(float))

        print("Scattering Function:")
        FDD = []
        for index in tqdm(range(self.count)):
            dir = self.dir + str(index)
            tempFDD = []
            with open(dir + "/funcionDeDispersion.csv") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    tempFDD.append(np.array(row).astype(float))
                    # temp_row = []
                    # for column in row:
                    #     temp_row.append(float(column))
                    # tempFDD.append(temp_row)
        FDD.append(np.array(tempFDD))

        PDDR = np.mean(PDDR, axis=0)
        FDA = np.mean(FDA, axis=0)
        DEDP = np.mean(DEDP, axis=0)
        FDCT = np.mean(FDCT, axis=0)
        FDD = np.mean(FDD, axis=0)
          

        if not os.path.exists(self.dir+"average"):
            os.makedirs(self.dir+"average")

        np.savetxt(self.dir + "average/perfilDePotenciaDeRetardo.csv", [PDDR], fmt='% s', delimiter=',', newline='\n')
        np.savetxt(self.dir + "average/correlacionDeFrecuencia.csv", [FDA], fmt='% s', delimiter=',', newline='\n')
        np.savetxt(self.dir + "average/densidadEspectralDePotencia.csv", [DEDP], fmt='% s', delimiter=',', newline='\n')
        np.savetxt(self.dir + "average/correlacionTemporal.csv", [FDCT], fmt='% s', delimiter=',', newline='\n')
        np.savetxt(self.dir + "average/funcionDeDispersion.csv", FDD, fmt='% s', delimiter=',', newline='\n')
        print("finished")
        #self.showGraphs(PDDR, CDF, DEDP, CT, FDD)
    
    
    def showGraphs(self, PDDR, FDA, DEDP, FDCT, FDD):
        #Mostrar gráficas
        # Perfil de potencia de retardo
        plt.plot((PDDR))
        plt.ylabel('Perfil de potecia de retardo')
        plt.show()

        # Autocorrelación de frecuencia
        plt.plot(np.fft.fftshift(FDA))
        plt.ylabel('Autocorrelación de frecuencia')
        plt.show()

        # Funcion de dispersion
        #Op.Mostrar("Funcion de dispersion", FDD, 2)
        fig = plt.figure()
        ax3d = plt.axes(projection="3d")

        xdata = np.linspace(0,10,11)
        ydata = np.linspace(0,1023,1024)
        ydata = np.fft.fftshift(ydata)
        X,Y = np.meshgrid(xdata,ydata)

        ax3d = plt.axes(projection='3d')
        ax3d.plot_surface(X, Y, FDD, cmap='plasma')
        ax3d.set_title('Funcion de dispersion')
        ax3d.set_xlabel('X')
        ax3d.set_ylabel('Y')
        ax3d.set_zlabel('Z')
        
        plt.show() 

        # Densidad espectral de potencia
        plt.plot(np.fft.fftshift(DEDP))
        plt.ylabel('Densidad espectral de potencia')
        plt.show()

        # Funcion de correlacion temporal
        plt.plot(np.fft.fftshift(FDCT))

        plt.ylabel('Funcion de correlacion temporal')
        plt.show()
