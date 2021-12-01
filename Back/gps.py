from numpy import float64
import serial
#from serial.serialutil import XOFF
import threading
import signal
import time


class Gps(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, daemon=True)
        self.shutdown_flag = threading.Event()
        self.data_lock = threading.Lock()
        self.data_lock.acquire()
        self.ActualLatitude = 0
        self.ActualLongitude = 0
        self.data_lock.release()
    
    def run(self):
        try:
            ser = serial.Serial('COM5', 9600, timeout=2)
            ser.flushInput()
            print("gps listening")
        except Exception as e:
            print("cant not connect to the gps via COM3")
            print(e)
        else:
            while not self.shutdown_flag.is_set():
                try:
                    ser_bytes = ser.readline()
                    decoded_bytes = ser_bytes[0:len(ser_bytes)-2].decode("utf-8")
                    splited_decoded = decoded_bytes.split(',')
                    if splited_decoded[0] == '$GNRMC':
                        type = splited_decoded[0]

                        self.data_lock.acquire()
                        self.time = splited_decoded[1]
                        self.data_lock.release()

                        self.state = True if splited_decoded[2]=="A" else False
                        latitude = splited_decoded[3]
                        longitude = splited_decoded[5]
                        
                        if self.state:
                            dotLa = latitude.find('.')
                            dotLo = longitude.find('.')

                            latitudeGrados = latitude[:dotLa-2]
                            longitudeGrados = longitude[:dotLo-2]

                            latiudeMinutos = latitude[dotLa-2:]
                            longitudeMinutos = longitude[dotLo-2:]

                            latiudeMinutos = str(float(latiudeMinutos)/60)
                            longitudeMinutos = str(float(longitudeMinutos)/60)

                            latitude = latitudeGrados + latiudeMinutos[1:]
                            longitude = longitudeGrados + longitudeMinutos[1:]

                            if splited_decoded[4] == "S":
                                latitude = "-" + latitude
                            if splited_decoded[6] == "W":
                                longitude = "-" + longitude
                            print(f"({latitude}, {longitude})")
                            #print(decoded_bytes)
                            self.data_lock.acquire()
                            self.ActualLatitude = latitude
                            self.ActualLongitude = longitude
                            self.data_lock.release()
                        else:
                            print("No gps signal\t", end='')
                            print(decoded_bytes)
                    
                except ValueError:
                    print(ValueError)
                    print("Keyboard Interrupt")
                    break
            print("gps off")

    def getPosition(self):
        return (self.ActualLatitude, self.ActualLongitude)
    def getTime(self):
        return (self.time)

class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    pass
 
 
def service_shutdown(signum, frame):
    print('Caught signal %d' % signum)
    raise ServiceExit

if __name__ == "__main__":
    # Register the signal handlers
    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)
    try:
        serv = Gps()
        serv.start()
        print("Manual gps start")
        while True:
            time.sleep(0.5)
    except ServiceExit:
        serv.shutdown_flag.set()
        serv.join()
        print("End")