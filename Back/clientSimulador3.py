from cProfile import run
from mimetypes import init
import threading
import numpy as np
import socket
import matplotlib.pyplot as plt
import numpy as np
from numpy.core.fromnumeric import size
from numpy.core.function_base import linspace
import cmath
import sys
np.set_printoptions(threshold=sys.maxsize)
import csv
from scipy import signal
import time
from tqdm import tqdm

class NewClient(threading.Thread):
    def __init__(self, Fmax, Fs, N):
        threading.Thread.__init__(self, daemon=False)
        self.shutdown_flag = threading.Event()
        self.data_lock = threading.Lock()
        ip = 'localhost'
        self.server_address = (ip, 10000)


        ######################
        #self.Fs = Fs
        self.Fs_G = Fs
        self.Fmax_G = Fmax
        self.N_G = N

        # #Cost 207 Model (Tux)
        # #Prueba con variaciones
        # self.delay = np.array([0,0.217,0.512,0.514,0.517,0.674,0.882,1.230,1.287,1.311,1.349,1.533,1.535,1.1622,1.818,1.836,1.884,1.943,2.048,2.140])*1e-6 
        # np.random.shuffle(self.delay)
        # pw_db = np.array([-5.7,-7.6,-10.1,-10.2,-10.2,-11.5,-13.4,-16.3,-16.9,-17.1,-17.4,-19,-19,-19.8,-21.5,-21.6,-22.1,-22.6,-23.5,-24.3])
        # np.random.shuffle(pw_db)
        # self.pw_lineal = 10**(pw_db/10)

        # TauMax = self.delay[-1] #Retardo Maximo
        # #TauMax = np.max(self.delay)

        # self.M=np.size(self.delay)
        # #N=2000
        # self.N = N
        # self.L=TauMax*Fs
        # self.L = int(np.floor(self.L))

        
        
        

        # ##############################JAKES###########################
        # #Introducimos el filtro FIR de distribución Jakes a cada uno de los coeficientes de x_q y x_i 
        # Fs_J = 5e5
        # N1=20001
        # N_Hamming=2001
        # f_lin = (np.linspace(-Fs_J/2,Fs_J/2,N1)) #O bien define tu linspace como complejo (?)
        # #Fmax = FMax
        # Sc_LambdaT = (1/((np.pi)*Fmax*(np.sqrt(1-((np.complex64(f_lin)/Fmax)**2))+0.0000001)))  #np.sqrt no puede lidiar con complejos, solo cmath.sqrt
        # #Necesitamos la parte real y luego todo fuera de Fmax debe ser 0 
        # Sc_LambdaT = np.real(Sc_LambdaT)
        # Sc_LambdaT[abs(f_lin)>=Fmax] = 0
        # Hf = np.sqrt(Sc_LambdaT)
        # Hf_FL = np.fft.fftshift(np.fft.ifft(np.fft.ifftshift(Hf)))
        # window = np.hamming(N_Hamming)
        # window = np.pad(window, (9000,9000), 'constant', constant_values=(0,0))

        # self.hfw = Hf_FL*window

        # self.hfw = self.hfw[self.hfw != 0]

        # self.hfw = self.hfw / np.linalg.norm(self.hfw) #Normalizamos

        # ##############Jakes############
    
    
    def run(self):

        while not self.shutdown_flag.is_set():
          h = []
          for n in tqdm(range(100)):
              h.append(self.newH())
          #Espera en tiempo real 

          #print(h)

          snooze = 1
          print(f"waiting...{snooze} seconds")
          snooze /= 100
          for n in tqdm(range(100)):
              time.sleep(snooze)

          #Intentar enviar algo

          # Connect the socket to the port where the server is listening
          print('connecting to {} port {}'.format(*self.server_address))
          sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          sock.connect(self.server_address)
          try:
              # Send data
              h2 = np.array(h, dtype=np.complex64)
              header = f"np.{h2.dtype.name};{h2.shape}"
              header = f"{header:<{32}}"
              print(header)
              msg = bytes(header, "utf-8") + h2.tobytes() + bytes("end","utf-8")
              print(f'sending {len(msg)} bytes')
              sock.sendall(msg)
          finally:
              print('closing socket')
              sock.close()
              print("end")




    def newH(self):
        ## Prueba: Recalcular ##
        self.Fs = self.Fs_G
        Fmax = self.Fmax_G

        #Cost 207 Model (Tux)
        #Prueba con variaciones + random seed
        rng = np.random.default_rng(np.random.randint(1,150,1))

        #self.delay = np.array([0,0.217,0.512,0.514,0.517,0.674,0.882,1.230,1.287,1.311,1.349,1.533,1.535,1.1622,1.818,1.836,1.884,1.943,2.048,2.140])*1e-6 
        #self.delay = np.random.uniform(0,2.5,[1,20])*1e-6
        #self.delay = np.array([0.3,0.5,0.63,0.72,0.856,0.957,1.05,1.12,1.20,1.23,1.29,1.44,1.50,1.57,1.68,1.77,1.81,1.92,2.14,2.33])*1e-6 #Si da distinto comportamiento

        delay = np.zeros(20)
        delay[0] = 0 + np.random.randint(1,4,1)*0.1 + np.random.randint(1,10,1)*0.01
        for i in range(1,20):
            delay[i] = delay[i-1] + np.random.randint(0,2,1)*0.1 + np.random.randint(1,10,1)*0.01

        self.delay = delay*1e-6

        rng.shuffle(self.delay)

        #pw_db = np.array([-5.7,-7.6,-10.1,-10.2,-10.2,-11.5,-13.4,-16.3,-16.9,-17.1,-17.4,-19,-19,-19.8,-21.5,-21.6,-22.1,-22.6,-23.5,-24.3])
        #pw_db = np.random.uniform(-5,-25,[1,20])
        #pw_db = np.random.randint(-25,-5,20)
        #pw_db = np.array([-2.4,-3.5,-7.1,-8.4,-10.6,-11.2,-13.5,-15.4,-17.1,-18.5,-19.7,-20.6,-21.5,-22.1,-23.3,-25.4,-27.9,-29.2,-30.3,-31.3]) #Si da distinto comportamiento

        db = np.zeros(20)
        db[0] = np.random.randint(1,4,1)*-1 + np.random.randint(1,10,1)*-0.1
        for i in range(1,20):
            db[i] = db[i-1] + np.random.randint(0,2,1)*-1 + np.random.randint(1,10,1)*-0.1

        pw_db = db

        rng.shuffle(pw_db)

        self.pw_lineal = 10**(pw_db/10)

        #TauMax = self.delay[-1] #Retardo Maximo
        #TauMax = np.max(self.delay)
        TauMax = 3.00*1e-6

        self.M = np.size(self.delay)
        #N=2000

        self.N = self.N_G

        self.L=TauMax*self.Fs
        self.L = int(np.floor(self.L))

        ##############################JAKES###########################
        #Introducimos el filtro FIR de distribución Jakes a cada uno de los coeficientes de x_q y x_i 
        Fs_J = 5e5
        N1=20001
        N_Hamming=2001
        f_lin = (np.linspace(-Fs_J/2,Fs_J/2,N1)) #O bien define tu linspace como complejo (?)
        #Fmax = FMax
        Sc_LambdaT = (1/((np.pi)*Fmax*(np.sqrt(1-((np.complex64(f_lin)/Fmax)**2))+0.0000001)))  #np.sqrt no puede lidiar con complejos, solo cmath.sqrt
        #Necesitamos la parte real y luego todo fuera de Fmax debe ser 0 
        Sc_LambdaT = np.real(Sc_LambdaT)
        Sc_LambdaT[abs(f_lin)>=Fmax] = 0
        Hf = np.sqrt(Sc_LambdaT)
        Hf_FL = np.fft.fftshift(np.fft.ifft(np.fft.ifftshift(Hf)))
        window = np.hamming(N_Hamming)
        window = np.pad(window, (9000,9000), 'constant', constant_values=(0,0))

        self.hfw = Hf_FL*window

        self.hfw = self.hfw[self.hfw != 0]

        self.hfw = self.hfw / np.linalg.norm(self.hfw) #Normalizamos

        ##############Jakes############
        ##Termina Prueba: Recalcular ##

        #Generar Matriz RNG de Paths
        #Distribución Normal con Media 0 y Varianza (Potencia) Unitaria
        mu = 0 #Media 
        var = potencia = 1 #Potencia 
        sigma = np.square(var) #Desviación Std

        #Estos dos representan un solo path, necesitamos M de estos, no estos de M tamaño

        x_q = np.zeros((self.N,self.M))
        x_i = np.zeros((self.N,self.M))

        for k in range(self.M):
            x_q[:,k] = np.random.normal(mu,sigma,self.N) #Digamos que esta es la ponderación de las sincs que vas a generar
            x_i[:,k] = np.random.normal(mu,sigma,self.N)

        x_i = x_i*1j
        #Necesitamos crear una matriz grande donde metamos todos los paths (Real+Imag) 
        x_iq = np.zeros((self.N,self.M),dtype='complex_')

        #Para cada valor de M vamos a filtrar un vector fila de tamaño N, luego sumar I + Q
        #Ese resultado lo metemos en x_iq 
        #Recordemos que lo importante es hacer toda la matriz NxM sin perder el estado 

        #Creamos estados iniciales para I y Q, valores en 0.
        zi_i = np.zeros(size(self.hfw)-1)
        zi_q = np.zeros(size(self.hfw)-1)

        #Ademas de variables que sostengan el estado
        zf_i = 0
        zf_q = 0

        #Necesitamos un ciclo que dure 'M' donde se filtre, se sume y se ingrese en x_iq 
        #ademas de conservar estados

        for i in range(self.M):
            xfilt_i, zf_i = signal.lfilter(self.hfw,1,x_i[:,i],zi=zi_i)
            xfilt_q, zf_q = signal.lfilter(self.hfw,1,x_q[:,i],zi=zi_q)

            x_iq[:,i] = xfilt_i + xfilt_q #Estos son los path coloreados

            zi_i = zf_i
            zi_q = zf_q

        #######Densidad Espectral de Potencia - Verif Jakes#######
        # file = open('C:/Users/Jesus/Desktop/path.csv', 'w')
        # writer = csv.writer(file)
        # writer.writerow(x_iq[:,1])
        # file.close
        ##########################################################

        #######Gráfica de Distribución#######
        #count, bins, ignored = plt.hist(abs(x_iq), 15, density=True)
        ##Distrib Rayleigh
        #plt.plot(bins, bins/(sigma**2) *  

        #               np.exp( -bins**2 / (2 * sigma**2) ),

        #         linewidth=2, color='r')

        #plt.show()
        ####################################

        #Generar Sincs

        space = linspace(0,self.L-1,self.L) #Linspace usando L es eje en muestras, necesita estar en tiempo
        Ts = 1/self.Fs
        t = space*Ts #Eje de Tiempo

        #Necesitamos hacer "M" sincs retrasadas según la variable de delay, en este caso son 20 sincs
        ML_Matrix = np.array(np.zeros(shape=(self.L,self.M)))
        for i in range(self.M):
            ML_Matrix[:,i] = np.sqrt(self.pw_lineal[i])*np.sinc((t-(self.delay[i]))*self.Fs) #Restar a 't' en la sinc es desplazar, multiplicar por Fs es ponderar
            

        #taps = np.zeros((self.L,self.N),dtype='complex_')

        taps = np.zeros((self.N,self.L),dtype='complex_')

        # for k in range(self.N):
        #     taps[:,k] = ML_Matrix@np.transpose(x_iq[k,:]) 

        for k in range(self.N):
            taps[k,:] = ML_Matrix@np.transpose(x_iq[k,:])

        # file = open('C:/Users/Jesus/Desktop/psd.csv', 'w')
        # writer = csv.writer(file)
        # for p in range(self.N):
        #     writer.writerow(taps[:,p])

        #np.savetxt('C:/Users/Jesus/Desktop/psd.csv', (taps), fmt='% s', delimiter=',', newline='\n')
        #file.close

        #print(np.shape(taps))
        return taps
