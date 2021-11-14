from types import coroutine
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QByteArray, QUrl, Qt
from folium.map import Tooltip
from Back.server import Server
from VISTA.UI.ui_main import Ui_FrmMain
from VISTA.vSettings import Vsettings
from VISTA.vOpenFile import VopenFile
import pandas as pd
import folium # pip install folium
import matplotlib.pyplot as plt
from PyQt5.QtWebEngineWidgets import QWebEngineView # pip install PyQtWebEngine
import sys
import io
import numpy as np
import csv
import plotly.express as px
import json
import os
from base64 import b64encode
import branca

from Back import server
class Principal(QDialog):

    def __init__(self):
        super().__init__()
        self.status = False
        self.G1 = "none"
        self.G2 = "none"

        self.inicializar_gui()
    
    def inicializar_gui(self):
        self.ui = Ui_FrmMain()
        self.Vsetting = Vsettings()
        self.VopenFile = VopenFile()
        self.ui.setupUi(self)
        

        #Botones Generales Record
        self.ui.btnSettings.clicked.connect(self.Vsetting.mostrar)
        self.ui.btnRec.clicked.connect(self.StartSesion)
        self.ui.pushButton_4.clicked.connect(self.saveFile)

        #Botones Generales Replay
        self.ui.btnPlay.clicked.connect(lambda: self.alertar("Elemento en contruccion"))
        self.ui.btnPause.clicked.connect(lambda: self.alertar("Elemento en contruccion"))
        self.ui.btnOpenFile.clicked.connect(self.getCSV)

        #Botones REC Grafica 1

        self.ui.rBtnMapRec1.clicked.connect(self.viewMap)
        self.ui.rBtnPDDRRec1.clicked.connect(lambda: self.alertar("Elemento en contruccion"))
        self.ui.rBtnFDDRec1.clicked.connect(lambda: self.alertar("Elemento en contruccion"))
        self.ui.rBtnFDARec1.clicked.connect(lambda: self.alertar("Elemento en contruccion")) 
        self.ui.rBtnDEDPRec1.clicked.connect(lambda: self.alertar("Elemento en contruccion"))
        self.ui.rBtnFDCTRec1.clicked.connect(lambda: self.alertar("Elemento en contruccion"))

        #Botones REC Grafica 2

        self.ui.rBtnMapRec2.clicked.connect(self.viewMap)
        self.ui.rBtnPDDRRec2.clicked.connect(lambda: self.alertar("Elemento en contruccion"))
        self.ui.rBtnFDDRec2.clicked.connect(lambda: self.alertar("Elemento en contruccion"))
        self.ui.rBtnFDARec2.clicked.connect(lambda: self.alertar("Elemento en contruccion")) 
        self.ui.rBtnDEDPRec2.clicked.connect(lambda: self.alertar("Elemento en contruccion"))
        self.ui.rBtnFDCTRec2.clicked.connect(lambda: self.alertar("Elemento en contruccion"))

        #Botones Replay Grafica 1

        self.ui.rBtnMapRep1.clicked.connect(self.viewMap) 
        self.ui.rBtnPDDRRep1.clicked.connect(lambda: self.plot("PDDR", "1", "0"))
        self.ui.rBtnFDDRep1.clicked.connect(lambda: self.plot("FDD", "1", "0"))
        self.ui.rBtnFDARep1.clicked.connect(lambda: self.plot("FDA", "1", "0")) 
        self.ui.rBtnDEDPRep1.clicked.connect(lambda: self.plot("DEDP", "1", "0"))
        self.ui.rBtnFDCTRep1.clicked.connect(lambda: self.plot("FDCT", "1", "0"))

        #Botones Replay Grafica 2

        self.ui.rBtnMapRep2.clicked.connect(self.viewMap)
        self.ui.rBtnPDDRRep2.clicked.connect(lambda: self.plot("PDDR", "2", "0"))
        self.ui.rBtnFDDRep2.clicked.connect(lambda: self.plot("FDD", "2", "0"))
        self.ui.rBtnFDARep2.clicked.connect(lambda: self.plot("FDA", "2", "0")) 
        self.ui.rBtnDEDPRep2.clicked.connect(lambda: self.plot("DEDP", "2", "0"))
        self.ui.rBtnFDCTRep2.clicked.connect(lambda: self.plot("FDCT", "2", "0"))

        self.ui.horizontalSlider.valueChanged.connect(self.valuechange)

        self.show()
    def valuechange(self):
        size = self.ui.horizontalSlider.value()
        print(size, self.G1, self.G2)
        if self.G1 != "none":
            self.plot(self.G1, "1", str(size))
        if self.G2 != "none":
            self.plot(self.G2, "2", str(size))

    def alertar(self,texto):
        mensaje = QMessageBox(self)
        mensaje.setWindowTitle('Mensaje')
        mensaje.setIcon(QMessageBox.Warning)
        mensaje.setText(texto)
        mensaje.exec_()

    def getCSV(self):
        # this will get only the header file, with the header file will know all the information necesary to show the record of a sesion
        filePath, _ = QFileDialog.getOpenFileName(self, 'Open file', '', filter="*.json")
        if filePath != "":
            print ("Dirección",filePath) 
            self.info = json.load(open(filePath))
            self.graphsRoute = os.path.dirname(filePath) + self.info['dir']
            #print(self.info)
            self.coordinates = []
            for c in self.info['coordenates']:
                self.coordinates.append((float(c[0]), float(c[1])))
            print(self.coordinates)
            self.alertar("Archivo cargado")

    def plot(self, graph, Wview, index):
        if Wview == "1":
            self.G1 = graph
        if Wview == "2":
            self.G2 = graph
        graphRoute = self.graphsRoute + index
        self.setSlider(int(self.info['size']))
        # Switch
        print(graph)
        if graph == "FDA":
            graphRoute += "/correlacionDeFrecuencia.csv"
        if graph == "PDDR":
            graphRoute += "/perfilDePotenciaDeRetardo.csv"
        if graph == "DEDP":
            graphRoute += "/densidadEspectralDePotencia.csv"
        if graph == "FDD":
            graphRoute += "/funcionDeDispersion.csv"
        if graph == "FDCT":
            graphRoute += "/correlacionTemporal.csv"
        
        with open(graphRoute) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for x in csv_reader:
                    self.df = np.array(x).astype(float)

        buffer = io.StringIO()
        #print(self.df)
        fig = px.scatter(x=np.linspace(0, self.df.size-1, self.df.size), y=np.fft.fftshift(self.df))
        fig.update_layout(hovermode="x")
        fig.update_traces(mode="markers+lines", hovertemplate=None)
        fig.update_layout(
            hoverlabel=dict(
                font_size=50,
                font_family="Rockwell"
            )
        )
        fast = False
        if fast:
            img_bytes = fig.to_image(format="png")
            encoding = b64encode(img_bytes).decode()
            img_b64 = "data:image/png;base64," + encoding
            html = ('''
            <html>
                <head>
                    <style>
                        *{
                            margin: 0;
                            padding: 0;
                        }
                    </style>
                </head>
                <body>
                    <img src="'''
                    + img_b64 + 
                '''" style="width:100%; max-height:100vh"/>
                </body>
            </html>''')
            if Wview == "1":
                self.ui.WRepG1.setZoomFactor(1)
                self.ui.WRepG1.setHtml(html)
            if Wview == "2":
                self.ui.WRepG2.setZoomFactor(1)
                self.ui.WRepG2.setHtml(html)
        else:
            fig.write_html(buffer, include_plotlyjs='directory', full_html=False)

            html = ('''
            <html style='margin: 0; padding:0'>
                <head>
                    <style>
                        *{
                            margin: 0;
                            padding: 0;
                        }
                        .modebar{
                            display: block !important;
                            margin: auto !important;
                            position: static !important;
                        }
                        .modebar-container {
                            display: flex;
                        }
                        .ytick text{
                            font-size: 1.8em !important;
                        }
                        .xtick text{
                            font-size: 1.8em !important;
                        }
                        .modebar-btn{
                            font-size: 2em !important;
                        }
                    </style>
                </head>
                <body>
                    <div style='position: fixed; width: 100%; height: 100vh; margin:0; padding:0'>'''
                    + buffer.getvalue() + 
                '''\n</div>
                </body>
            </html>''')

            url = QUrl(os.path.abspath(__file__).replace(os.sep, '/'))
            if Wview == "1":
                self.ui.WRepG1.setZoomFactor(0.5)
                self.ui.WRepG1.setHtml(html, baseUrl=url)
            if Wview == "2":
                self.ui.WRepG2.setZoomFactor(0.5)
                self.ui.WRepG2.setHtml(html, baseUrl=url)
        
    def saveFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)
    
    def viewMap(self):
        self.coordinate = self.coordinates[0]
        self.m = folium.Map(
        	tiles='Stamen Toner',
        	zoom_start=15,
        	location=self.coordinate
        )
        #html = "<p>Latitud: 20.628269</p><p>Longitud: -103.284029</p>"
        #iframe1 = branca.element.IFrame(html=html, width=300, height=100)
        for coord in self.coordinates:
            self.marcado = folium.Marker(location=coord,
            popup=self.coordinate,tooltip=Tooltip,
            icon=folium.Icon(color="red")).add_to(self.m)
        # save map data to data object
        self.data = io.BytesIO()
        self.m.save(self.data, close_file=False)
        #switch(self.ui.)
        
        if self.ui.rBtnMapRec1.isChecked():
            self.ui.WRecG1.setHtml(self.data.getvalue().decode())
        if self.ui.rBtnMapRec2.isChecked():
            self.ui.WRecG2.setHtml(self.data.getvalue().decode())
        if self.ui.rBtnMapRep1.isChecked():
            self.ui.WRepG1.setHtml(self.data.getvalue().decode())
        if self.ui.rBtnMapRep2.isChecked():
            self.ui.WRepG2.setHtml(self.data.getvalue().decode())
        #self.addWidget(webView)

    def StartSesion(self):
        if not self.status:
            self.name, self.estado = QInputDialog.getText(self,"Sesion", "Nombre de la Sesion:")
            if self.name and self.estado != '' : 
                print('Nombre:', self.name)
            self.status = True
            self.serv = Server()
            self.serv.start()
            self.ui.btnRec.setStyleSheet("border-image: url(:/botones/BotonStop.jpg);")
        else:
            self.status = False
            self.serv.shutdown_flag.set()
            self.serv.join()
            self.ui.btnRec.setStyleSheet("border-image: url(:/botones/BotonRec.jpg);")
            self.alertar("Sesion Finalizada")

            print("End")
    
    def setSlider(self,top):
        top -= 1
        self.ui.horizontalSlider.setMinimum(0)
        self.ui.horizontalSlider.setMaximum(top)
        self.ui.horizontalSlider.setTickInterval(top)
        self.ui.horizontalSlider.setTickPosition(QSlider.TicksBothSides)

def main():
    app = QApplication(sys.argv)
    ventana = Principal()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()