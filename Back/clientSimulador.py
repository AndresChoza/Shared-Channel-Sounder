from ctypes import sizeof
import socket
import csv
import numpy as np
import random as rd
import time
from tqdm import tqdm

# # Create a TCP/IP socket
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # Connect the socket to the port where the server is listening
# server_address = ('localhost', 10000)
# print('connecting to {} port {}'.format(*server_address))
# sock.connect(server_address)

#Dosificar Realizaciones
# Create a TCP/IP socket

ip = input()
server_address = (ip, 10000)
print("reading data...")
pool = []
ChannelRealizationFileName = "./ChannelRealizations/realizationArray"
for n in tqdm(range(100)):
    fileRoute = ChannelRealizationFileName + str(n+1) + ".csv"
    with open(fileRoute) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        temph = []
        for row in csv_reader:
            temprow = []
            for column in row:
                column = column.replace(" ","")
                column = column.replace("i","j")
                column = column.split("+")
                if column[1][0] == '-':
                    column = column[0] + column[1]
                else:
                    column = column[0] + "+" + column[1]
                temprow.append(complex(column))
            temph.append(temprow)
        pool.append(temph)
while(True):
    h = []
    for n in tqdm(range(500)):
        rand_Index = rd.randrange(0,100)
        h.append(pool[rand_Index])
    #Espera en tiempo real 
    snooze = rd.randrange(0,2)
    print(f"waiting...{snooze} seconds")
    snooze /= 100
    for n in tqdm(range(100)):
        time.sleep(snooze)

    #Intentar enviar algo

    # Connect the socket to the port where the server is listening
    print('connecting to {} port {}'.format(*server_address))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
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
