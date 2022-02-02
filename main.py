from logging import setLogRecordFactory 
from types import coroutine
#from PyQt5 import QtWidgets
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
import plotly.graph_objects as go
from jinja2 import Template
import time 
import threading
import signal

from Back import server
class Principal(QDialog):

    def __init__(self):
        super().__init__()
        self.status = False
        self.G1 = "none"
        self.G2 = "none"
        self.webView1 = QWebEngineView()
        self.webView2 = QWebEngineView()
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
        self.ui.btnPlay.clicked.connect(self.playGraph)
        self.ui.btnPause.clicked.connect(self.stopGraph)
        self.ui.btnOpenFile.clicked.connect(self.getJSON)

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
        self.ui.rBtnPDDRRep1.clicked.connect(lambda: self.changePlot("PDDR", "1"))
        self.ui.rBtnFDDRep1.clicked.connect(lambda: self.changePlot("FDD", "1"))
        self.ui.rBtnFDARep1.clicked.connect(lambda: self.changePlot("FDA", "1")) 
        self.ui.rBtnDEDPRep1.clicked.connect(lambda: self.changePlot("DEDP", "1"))
        self.ui.rBtnFDCTRep1.clicked.connect(lambda: self.changePlot("FDCT", "1"))

        #Botones Replay Grafica 2

        self.ui.rBtnMapRep2.clicked.connect(self.viewMap)
        self.ui.rBtnPDDRRep2.clicked.connect(lambda: self.changePlot("PDDR", "2"))
        self.ui.rBtnFDDRep2.clicked.connect(lambda: self.changePlot("FDD", "2"))
        self.ui.rBtnFDARep2.clicked.connect(lambda: self.changePlot("FDA", "2")) 
        self.ui.rBtnDEDPRep2.clicked.connect(lambda: self.changePlot("DEDP", "2"))
        self.ui.rBtnFDCTRep2.clicked.connect(lambda: self.changePlot("FDCT", "2"))

        #Botones Slider
        self.ui.btnSpeed1.clicked.connect(lambda: self.setSpeed(1))
        self.ui.btnSpeed5.clicked.connect(lambda: self.setSpeed(5))
        self.ui.btnSpeed10.clicked.connect(lambda: self.setSpeed(10))

        self.ui.horizontalSlider.valueChanged.connect(self.valuechange)
        
        self.show()
        self.i=0
        self.aux=0
        self.speed =1

    def playGraph(self):
        if self.i >= int(self.info['size']):
            self.i=self.aux = 0
            self.speed =1
        self.thread = threading.Timer(1.0,self.worker)
        self.thread.start()

    def setSpeed(self,velocidad): 
        self.speed = velocidad

    def worker(self):
        if self.i < int(self.info['size']):
            self.i+=self.speed
            self.aux = self.i
            self.ui.horizontalSlider.setValue(self.i)

            self.thread = threading.Timer(1.0,self.worker)
            self.thread.start()
        if self.aux != self.i:
            self.i = self.aux

    def stopGraph(self):
        self.i = int(self.info['size'])
        
    def valuechange(self):
        self.size = self.ui.horizontalSlider.value() 

        if self.G1 != "none" and self.G1 != "MAP1":
            self.plot(self.G1, "1", str(self.size))
        if self.G1 == "MAP1":
            self.add_marker(str(self.size),self.G1)
        if self.G2 != "none" and self.G2 != "MAP2":
            self.plot(self.G2, "2", str(self.size))
        if self.G2 == "MAP2":
             self.add_marker(str(self.size),self.G2)

    def alertar(self,texto):
        mensaje = QMessageBox(self)
        mensaje.setWindowTitle('Mensaje')
        mensaje.setIcon(QMessageBox.Warning)
        mensaje.setText(texto)
        mensaje.exec_()

    def getJSON(self):
        # this will get only the header file, with the header file will know all the information necesary to show the record of a sesion
        filePath, _ = QFileDialog.getOpenFileName(self, 'Open file', '', filter="*.json")
        if filePath != "":
            print ("Dirección",filePath) 
            self.info = json.load(open(filePath))
            self.graphsRoute = os.path.dirname(filePath) + self.info['dir']
            print(self.graphsRoute)
            self.setSlider(int(self.info['size']))
            self.coordinates = []
            for c in self.info['coordenates']:
                self.coordinates.append(tuple([float(c[0]), float(c[1])]))
            #print(self.coordinates)
            self.alertar("Archivo cargado")

    """def plot(self, graph, Wview, index):
        Fs = 5e6
        if Wview == "1":
            self.G1 = graph
        if Wview == "2":
            self.G2 = graph
        graphRoute = self.graphsRoute + index
        #self.setSlider(int(self.info['size']))
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

        buffer = io.StringIO()
        
        if graph == "FDA":
            with open(graphRoute) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for x in csv_reader:
                    df = np.array(x).astype(float)
            fig = px.scatter(x=np.linspace(-Fs/2, Fs/2 - Fs/df.size, df.size), y=np.roll(df, int(df.size/2)))
            fig.update_layout(hovermode="x")
            fig.update_traces(mode="markers+lines", hovertemplate=None)
            fig.update_layout(
                hoverlabel=dict(
                    font_size=50,
                    font_family="Rockwell"
                )
            )
            fig.update_xaxes(
                title="Δf",
                titlefont=dict(
                    size=30
                ),
                tickfont = dict(
                    size= 25
                ), 
            )
            fig.update_yaxes(
                title="Índice",
                titlefont=dict(
                    size=30
                ),
                tickfont = dict(
                    size= 25
                )
            )
        if graph == "PDDR":
            with open(graphRoute) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for x in csv_reader:
                    df = np.array(x).astype(float)
            fig = px.scatter(x=np.linspace(0, 1/Fs, df.size), y=df)
            fig.update_layout(hovermode="x")
            fig.update_traces(mode="markers+lines", hovertemplate=None)
            fig.update_layout(
                hoverlabel=dict(
                    font_size=50,
                    font_family="Rockwell"
                )
            )
            fig.update_xaxes(
                title="Retardos",
                titlefont=dict(
                    size=30
                ),
                showexponent = 'all',
                tickformat = '.0e',
                rangemode = 'tozero',
                tickfont = dict(
                    size= 25
                ), 
                tickangle=30
            )
            fig.update_yaxes(
                title="Potencia Normalizada",
                titlefont=dict(
                    size=30
                ),
                tickfont = dict(
                    size= 25
                )
            )
        if graph == "DEDP":
            with open(graphRoute) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for x in csv_reader:
                    df = np.array(x).astype(float)
            fig = px.scatter(x=np.linspace(-Fs/2, Fs/2 - 1, df.size), y=np.roll(df, int(df.size/2)) + 1, log_y=True)
            fig.update_layout(hovermode="x")
            fig.update_traces(mode="markers+lines", hovertemplate=None)
            fig.update_layout(
                hoverlabel=dict(
                    font_size=50,
                    font_family="Rockwell"
                )
            )
            fig.update_xaxes(
                title="Hz",
                titlefont=dict(
                    size=30
                ),
                tickfont = dict(
                    size= 25
                ), 
            )
            fig.update_yaxes(
                title="dB/Hz",
                titlefont=dict(
                    size=30
                ),
                tickfont = dict(
                    size= 25
                )
            )
        if graph == "FDCT":
            with open(graphRoute) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for x in csv_reader:
                    df = np.array(x).astype(float)
            fig = px.scatter(x=np.linspace(0, Fs-1, df.size), y=np.fft.fftshift(df))
            fig.update_layout(hovermode="x")
            fig.update_traces(mode="markers+lines", hovertemplate=None)
            fig.update_layout(
                hoverlabel=dict(
                    font_size=50,
                    font_family="Rockwell"
                )
            )
            fig.update_xaxes(
                title="",
                titlefont=dict(
                    size=30
                ),
                tickfont = dict(
                    size= 25
                ), 
            )
            fig.update_yaxes(
                title="Correlación normalizada",
                titlefont=dict(
                    size=30
                ),
                tickfont = dict(
                    size= 25
                )
            )
        if graph == "FDD":
            z_data = pd.read_csv(graphRoute)
            fig = go.Figure(
                data=[
                    go.Surface(z=np.fft.fftshift(z_data.values, axes=0), x = np.linspace(0, int(z_data.shape[1]), int(z_data.shape[1])+1), y = np.linspace(-(int(z_data.shape[0])+1)/2, (int(z_data.shape[0])+1)/2, int(z_data.shape[0])+1))
                    ]
                )
            fig.update_layout(
                    title='', autosize=True,
                    width=850, height=550,
                    margin=dict(l=65, r=50, b=65, t=90),
                    xaxis=dict(
                        title="x_value",
                        titlefont=dict(
                            size=40
                        )
                    ),
                    yaxis=dict(
                        title="y_value",
                        titlefont=dict(
                            size=40
                        )
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
                self.webView1.setZoomFactor(1)
                self.webView1.setHtml(html)
                self.ui.vLRepG1.addWidget(self.webView1)
               
            if Wview == "2":
                self.webView2.setZoomFactor(1)
                self.webView2.setHtml(html)
                self.ui.vLRepG2.addWidget(self.webView2)
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
                        .modebar-btn{
                            font-size: 2em !important;
                        }
                    </style>
                </head>
                <body>
                    <div style='position: fixed; width: 100%; height: 100vh; margin:0; padding:0; display:flex; justify-content:center'>'''
                    + buffer.getvalue() + 
                '''\n</div>
                </body>
            </html>''')
            f = open("graph.html", "w")
            f.write(html)
            f.close()
            url = QUrl(os.path.abspath(__file__).replace(os.sep, '/'))
            if Wview == "1":
                self.webView1.setZoomFactor(0.5)
                self.webView1.setHtml(html, baseUrl=url)
                self.ui.vLRepG1.addWidget(self.webView1)
            if Wview == "2":
                self.webView2.setZoomFactor(0.5)
                self.webView2.setHtml(html, baseUrl=url)
                self.ui.vLRepG2.addWidget(self.webView2)"""
    def changePlot(self, graph, Wview):
        self.plot(graph, Wview, str(self.ui.horizontalSlider.value()))
        pass
    def plot(self, graph, Wview, index):
        Fs = 5e6
        if Wview == "1":
            self.G1 = graph
        if Wview == "2":
            self.G2 = graph
        graphRoute = self.graphsRoute + index
        #self.setSlider(int(self.info['size']))
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

        buffer = io.StringIO()
        #print(self.df)
        if graph == "FDA":
            with open(graphRoute) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for x in csv_reader:
                    df = np.array(x).astype(float)
            fig = px.scatter(x=np.linspace(-Fs/2, Fs/2 - Fs/df.size, df.size), y=np.roll(df, int(df.size/2)))
            fig.update_layout(hovermode="x")
            fig.update_traces(mode="markers+lines", hovertemplate=None)
            fig.update_layout(
                hoverlabel=dict(
                    font_size=50,
                    font_family="Rockwell"
                )
            )
            fig.update_xaxes(
                title="Δf",
                titlefont=dict(
                    size=30
                ),
                tickfont = dict(
                    size= 25
                ), 
            )
            fig.update_yaxes(
                title="Índice",
                titlefont=dict(
                    size=30
                ),
                tickfont = dict(
                    size= 25
                )
            )
        if graph == "PDDR":
            with open(graphRoute) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for x in csv_reader:
                    df = np.array(x).astype(float)
            fig = px.scatter(x=np.linspace(0, 1/Fs, df.size), y=df)
            fig.update_layout(hovermode="x")
            fig.update_traces(mode="markers+lines", hovertemplate=None)
            fig.update_layout(
                hoverlabel=dict(
                    font_size=50,
                    font_family="Rockwell"
                )
            )
            fig.update_xaxes(
                title="Retardos",
                titlefont=dict(
                    size=30
                ),
                showexponent = 'all',
                tickformat = '.0e',
                rangemode = 'tozero',
                tickfont = dict(
                    size= 25
                ), 
                tickangle=30
            )
            fig.update_yaxes(
                title="Potencia Normalizada",
                titlefont=dict(
                    size=30
                ),
                tickfont = dict(
                    size= 25
                )
            )
        if graph == "DEDP":
            with open(graphRoute) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for x in csv_reader:
                    df = np.array(x).astype(float)
            fig = px.scatter(x=np.linspace(-Fs/2, Fs/2 - 1, df.size), y=np.roll(df, int(df.size/2)) + 1, log_y=True)
            fig.update_layout(hovermode="x")
            fig.update_traces(mode="markers+lines", hovertemplate=None)
            fig.update_layout(
                hoverlabel=dict(
                    font_size=50,
                    font_family="Rockwell"
                )
            )
            fig.update_xaxes(
                title="Hz",
                titlefont=dict(
                    size=30
                ),
                tickfont = dict(
                    size= 25
                ), 
            )
            fig.update_yaxes(
                title="dB/Hz",
                titlefont=dict(
                    size=30
                ),
                tickfont = dict(
                    size= 25
                )
            )
        if graph == "FDCT":
            with open(graphRoute) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for x in csv_reader:
                    df = np.array(x).astype(float)
            fig = px.scatter(x=np.linspace(0, Fs-1, df.size), y=np.fft.fftshift(df))
            fig.update_layout(hovermode="x")
            fig.update_traces(mode="markers+lines", hovertemplate=None)
            fig.update_layout(
                hoverlabel=dict(
                    font_size=50,
                    font_family="Rockwell"
                )
            )
            fig.update_xaxes(
                title="",
                titlefont=dict(
                    size=30
                ),
                tickfont = dict(
                    size= 25
                ), 
            )
            fig.update_yaxes(
                title="Correlación normalizada",
                titlefont=dict(
                    size=30
                ),
                tickfont = dict(
                    size= 25
                )
            )
        if graph == "FDD":
            z_data = pd.read_csv(graphRoute)
            fig = go.Figure(
                data=[
                    go.Surface(z=np.fft.fftshift(z_data.values, axes=0), x = np.linspace(0, int(z_data.shape[1]), int(z_data.shape[1])+1), y = np.linspace(-(int(z_data.shape[0])+1)/2, (int(z_data.shape[0])+1)/2, int(z_data.shape[0])+1))
                    ]
                )
            fig.update_layout(
                    title='', autosize=True,
                    width=850, height=550,
                    margin=dict(l=65, r=50, b=65, t=90),
                    xaxis=dict(
                        title="x_value",
                        titlefont=dict(
                            size=40
                        )
                    ),
                    yaxis=dict(
                        title="y_value",
                        titlefont=dict(
                            size=40
                        )
                    )
                )
        url = QUrl(os.path.abspath(__file__).replace(os.sep, '/'))
        html = fig.to_html(include_plotlyjs='directory')
        if Wview == "1":
            self.webView1.setZoomFactor(0.5)
            self.webView1.setHtml(html, baseUrl=url)
            self.ui.vLRepG1.addWidget(self.webView1)
        
        if Wview == "2":
            self.webView2.setZoomFactor(0.5)
            self.webView2.setHtml(html, baseUrl=url)
            self.ui.vLRepG2.addWidget(self.webView2)
        
        f = open("graph"+Wview+".html", "w")
        f.write(html)
        f.close()

    def saveFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)
    
    def viewMap(self):
        self.size = self.ui.horizontalSlider.value()
        self.m = folium.Map(
        	tiles=#'Stamen Toner',
            'Stamen Terrain',
        	zoom_start=15,
        	location= self.coordinates[int(self.size)]
            )
        marker = folium.Marker(location=self.coordinates[int(self.size)]).add_to(self.m)
        folium.PolyLine(self.coordinates, color="red", weight=3, opacity=1).add_to(self.m)
        # save map data to data object
        self.data = io.BytesIO()
        self.m.save(self.data, close_file=False)
        #switch(self.ui.)
        if self.ui.rBtnMapRec1.isChecked():
            self.ui.WRecG1.setHtml(self.data.getvalue().decode())

        if self.ui.rBtnMapRec2.isChecked():
            self.ui.WRecG2.setHtml(self.data.getvalue().decode())

        if self.ui.rBtnMapRep1.isChecked():
            self.webView1.setHtml(self.data.getvalue().decode())
            self.ui.vLRepG1.addWidget(self.webView1)
            self.G1 = "MAP1"
        if self.ui.rBtnMapRep2.isChecked():
            self.webView2.setHtml(self.data.getvalue().decode())
            self.ui.vLRepG2.addWidget(self.webView2)
            self.G2 = "MAP2"            

    def StartSesion(self):
        if not self.status:
            self.name, self.estado = QInputDialog.getText(self,"Sesion", "Nombre de la Sesion:")
            if self.estado: 
                print('Nombre:', self.name)
                self.status = True
                self.serv = Server(self.name)
                self.serv.start()
                self.updater = Updater(self.serv)
                self.updater.start()
                self.ui.btnRec.setStyleSheet("border-image: url(:/botones/BotonStop.jpg);")
        else:
            self.status = False
            self.serv.shutdown_flag.set()
            self.serv.join()
            self.updater.shutdown_flag.set()
            self.updater.join()
            self.ui.btnRec.setStyleSheet("border-image: url(:/botones/BotonRec.jpg);")
            self.alertar("Sesion Finalizada")

            print("End")
    
    def setSlider(self,top):
        top -= 1
        self.ui.horizontalSlider.setMinimum(0)
        self.ui.horizontalSlider.setMaximum(top)
        self.ui.horizontalSlider.setTickInterval(top)
        self.ui.horizontalSlider.setTickPosition(QSlider.TicksBothSides)

    def add_marker(self,point,Wview):
        self.fpoint = self.coordinates[int(point)]
        print(self.m.get_name())
        print(self.fpoint)
        if Wview == "MAP1":
            js = Template(
             """ 
             {{map}}.eachLayer(function (layer){
                 if(layer._icon)
                 {{map}}.removeLayer(layer);;});
                  marker = new L.marker([{{latitude}}, {{longitude}}] );
                {{map}}.addLayer(marker);
                {{map}}.setView([{{latitude}}, {{longitude}}],15);
        """
            ).render(map=self.m.get_name(), latitude=self.fpoint[0], longitude=self.fpoint[1])
            self.webView1.page().runJavaScript(js)

        if Wview == "MAP2":
            js = Template(
             """ 
             {{map}}.eachLayer(function (layer){
                 if(layer._icon)
                 {{map}}.removeLayer(layer);;});
                  marker = new L.marker([{{latitude}}, {{longitude}}] );
        {{map}}.addLayer(marker);
        {{map}}.setView([{{latitude}}, {{longitude}}],15);
        """
            ).render(map=self.m.get_name(), latitude=self.fpoint[0], longitude=self.fpoint[1])
            self.webView2.page().runJavaScript(js)

class Updater(threading.Thread):
    def __init__(self, serve):
        threading.Thread.__init__(self, daemon=True)
        self.shutdown_flag = threading.Event()
        self.serve = serve
    def run(self):
        while not self.shutdown_flag.is_set():
            time.sleep(1)
            if self.serve.newOp_flag.is_set():
                print("Hi new data is avaliabe")
                self.serve.newOp_flag.clear()
        print("stop of the updater")
            

    

def main():
    
    app = QApplication(sys.argv)
    ventana = Principal()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()