from PyQt5.QtWidgets import *
from .UI.ui_mensaje import  Ui_Form
import sys

class Vmensaje(QDialog):

    def __init__(self):
        super(Vmensaje, self).__init__()
        self.widgets =  Ui_Form()
        self.widgets.setupUi(self)

    def mostrar(self):
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Mensaje =  Ui_Form()
    Mensaje.show()
    sys.exit(app.exec_())