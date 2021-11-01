from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QByteArray, QUrl
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

from Back import server
class Principal(QDialog):

    def __init__(self):
        super().__init__()
        self.status = False
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
        self.ui.rBtnPDDRRep1.clicked.connect(lambda: self.plot("PDDR", "1"))
        self.ui.rBtnFDDRep1.clicked.connect(lambda: self.plot("FDD", "1"))
        self.ui.rBtnFDARep1.clicked.connect(lambda: self.plot("FDA", "1")) 
        self.ui.rBtnDEDPRep1.clicked.connect(lambda: self.plot("DEDP", "1"))
        self.ui.rBtnFDCTRep1.clicked.connect(lambda: self.plot("FDCT", "1"))

        #Botones Replay Grafica 2

        self.ui.rBtnMapRep2.clicked.connect(self.viewMap)
        self.ui.rBtnPDDRRep2.clicked.connect(lambda: self.plot("PDDR", "2"))
        self.ui.rBtnFDDRep2.clicked.connect(lambda: self.plot("FDD", "2"))
        self.ui.rBtnFDARep2.clicked.connect(lambda: self.plot("FDA", "2")) 
        self.ui.rBtnDEDPRep2.clicked.connect(lambda: self.plot("DEDP", "2"))
        self.ui.rBtnFDCTRep2.clicked.connect(lambda: self.plot("FDCT", "2"))

        self.show()

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
            print(self.info)
            self.alertar("Archivo cargado")

    def plot(self, graph, Wview):
        graphRoute = self.graphsRoute + "0"
        # Switch
        if graph == "FDA":
            graphRoute += "/correlacionDeFrecuencia.csv"
            lambda: self.setSlider(10)
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
        print(self.df)
        fig = px.scatter(x=np.linspace(0, self.df.size-1, self.df.size), y=np.fft.fftshift(self.df))
        fig.update_layout(hovermode="x")
        fig.update_traces(mode="markers+lines", hovertemplate=None)
        fig.update_layout(
            hoverlabel=dict(
                font_size=50,
                font_family="Rockwell"
            )
        )
        fast = True
        if fast:
            img_bytes = fig.to_image(format="png")
            encoding = b64encode(img_bytes).decode()
            img_b64 = "data:image/png;base64," + encoding
            html = ('''
            <html style='margin: 0; padding:0'>
                <head>
                    <style>
                    </style>
                </head>
                <body>
                    <img src="'''
                    + img_b64 + 
                '''" style="width:100%"/>
                </body>
            </html>''')
            self.ui.WRepG2.setHtml(html)
            pass
        else:
            fig.write_html(buffer, include_plotlyjs='directory', full_html=False)

            html = ('''
            <html style='margin: 0; padding:0'>
                <head>
                    <style>
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

            self.ui.WRepG2.setZoomFactor(0.5)
            self.ui.WRepG2.setHtml(html, baseUrl=url)
        
    def saveFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)
    
    def viewMap(self):
        coordinate = (20.628269,-103.284029)
        m = folium.Map(
        	tiles='Stamen Terrain',
        	zoom_start=15,
        	location=coordinate
        )

        # save map data to data object
        data = io.BytesIO()
        m.save(data, close_file=False)
        #switch(self.ui.)
        
        if self.ui.rBtnMapRec1.isChecked():
            self.ui.WRecG1.setHtml(data.getvalue().decode())
        if self.ui.rBtnMapRec2.isChecked():
            self.ui.WRecG2.setHtml(data.getvalue().decode())
        if self.ui.rBtnMapRep1.isChecked():
            self.ui.WRepG1.setHtml(data.getvalue().decode())
        if self.ui.rBtnMapRep2.isChecked():
            self.ui.WRepG2.setHtml(data.getvalue().decode())
        #self.addWidget(webView)

    def StartSesion(self):
        if not self.status:
            self.status = True
            self.serv = Server()
            self.serv.start()
            self.ui.btnRec.setStyleSheet("border-image: url(:/botones/BotonStop.jpg);")
        else:
            self.status = False
            self.serv.shutdown_flag.set()
            self.serv.join()
            self.ui.btnRec.setStyleSheet("border-image: url(:/botones/BotonRec.jpg);")

            print("End")
    
    def setSlider(self,top):
        self.ui.horizontalSlider.setMinimum(0)
        self.ui.horizontalSlider.setMaximum(top)
        self.ui.horizontalSlider.setTickInterval(2)

def main():
    app = QApplication(sys.argv)
    ventana = Principal()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()