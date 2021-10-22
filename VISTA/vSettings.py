from PyQt5.QtWidgets import *
from .UI.ui_settings import Ui_Dialog
import sys

class Vsettings(QDialog):

    def __init__(self):
        super(Vsettings, self).__init__()
        self.widgets = Ui_Dialog()
        self.widgets.setupUi(self)

    def mostrar(self):
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Settings = Ui_Dialog()
    Settings.show()
    sys.exit(app.exec_())