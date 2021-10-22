import folium # pip install folium
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView # pip install PyQtWebEngine
import sys
import io

class VMapa(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Folium in PyQt Example')
        self.window_width, self.window_height = 510, 400
        self.setMinimumSize(self.window_width, self.window_height)

        layout = QVBoxLayout()
        self.setLayout(layout)

        coordinate = (20.628269,-103.284029)
        m = folium.Map(
        	tiles='Stamen Terrain',
        	zoom_start=20,
        	location=coordinate
        )

        # save map data to data object
        data = io.BytesIO()
        m.save(data, close_file=False)

        webView = QWebEngineView()
        webView.setHtml(data.getvalue().decode())
        layout.addWidget(webView)

    def mostrar(self):
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Mapa = VMapa()
    Mapa.show()
    sys.exit(app.exec_())