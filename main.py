from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QUrl
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
class Principal(QDialog):

    def __init__(self):
        super().__init__()

        self.inicializar_gui()
    
    def inicializar_gui(self):
        self.ui = Ui_FrmMain()
        self.Vsetting = Vsettings()
        self.VopenFile = VopenFile()
        self.ui.setupUi(self)
        
        self.mensaje = QMessageBox(self)
        self.mensaje.setWindowTitle('Mensaje')

        #Botones Generales Record
        self.ui.btnSettings.clicked.connect(self.Vsetting.mostrar)
        self.ui.btnRec.clicked.connect(self.alertar)
        self.ui.pushButton_4.clicked.connect(self.saveFile)

        #Botones Generales Replay
        self.ui.btnPlay.clicked.connect(self.alertar)
        self.ui.btnPause.clicked.connect(self.alertar)
        self.ui.btnOpenFile.clicked.connect(self.getCSV)

        #Botones REC Grafica 1

        self.ui.rBtnMapRec1.clicked.connect(self.viewMap)
        self.ui.rBtn3DRec1.clicked.connect(self.alertar)
        self.ui.rBtnPDPRec1.clicked.connect(self.alertar)
        self.ui.rBtnPSPRec1.clicked.connect(self.alertar) 
        self.ui.radioButton_20.clicked.connect(self.alertar)
        self.ui.radioButton_24.clicked.connect(self.alertar)

        #Botones REC Grafica 2

        self.ui.rBtnMapRec2.clicked.connect(self.viewMap)
        self.ui.rBtn3DRec2.clicked.connect(self.alertar)
        self.ui.rBtnPDPRec2.clicked.connect(self.alertar)
        self.ui.radioButton_29.clicked.connect(self.alertar) 
        self.ui.radioButton_26.clicked.connect(self.alertar)
        self.ui.radioButton_30.clicked.connect(self.alertar) 

        #Botones Replay Grafica 1

        self.ui.rBtnMapRep1.clicked.connect(self.viewMap) 
        self.ui.rBtn3DRep1.clicked.connect(self.alertar)
        self.ui.rBtnPDPRep1.clicked.connect(self.alertar)
        self.ui.rBtnPSPRep1.clicked.connect(self.alertar)  
        self.ui.radioButton_14.clicked.connect(self.alertar)
        self.ui.radioButton_18.clicked.connect(self.alertar)

        #Botones Replay Grafica 2

        self.ui.rBtnMapRep2.clicked.connect(self.viewMap)
        self.ui.rBtn3DRep2.clicked.connect(self.alertar)
        self.ui.rBtnPDPRep2.clicked.connect(lambda: self.plot("DEDP"))
        self.ui.rBtnPSPRep2.clicked.connect(self.alertar)  
        self.ui.radioButton_10.clicked.connect(self.alertar)
        self.ui.radioButton_7.clicked.connect(self.alertar)

        self.show()

    def alertar(self):
        self.mensaje.setIcon(QMessageBox.Warning)
        self.mensaje.setText('Elemento en construccion')
        self.mensaje.exec_()

    def getCSV(self):
        # this will get only the header file, with the header file will know all the information necesary to show the record of a sesion
        filePath, _ = QFileDialog.getOpenFileName(self, 'Open file', '', filter="*.json")
        if filePath != "":
            print ("Dirección",filePath) 
            self.info = json.load(open(filePath))
            self.graphsRoute = os.path.dirname(filePath) + self.info['dir']
            print(self.info)
            

    def plot(self, graph):
        graphRoute = self.graphsRoute + "0"
        # Switch
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

        #url = QUrl("C:/Users/Jesus/Desktop/Shared work/Channel-Sounder/imgtest.html")
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

def main():
    app = QApplication(sys.argv)
    ventana = Principal()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()