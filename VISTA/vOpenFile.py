from PyQt5.QtWidgets import *
from .UI.ui_openFile import Ui_Dialog
import sys

class VopenFile(QDialog):

    def __init__(self):
        super(VopenFile, self).__init__()
        self.widgets = Ui_Dialog()
        self.widgets.setupUi(self)

    def mostrar(self):
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    openFile = Ui_Dialog()
    openFile.show()
    sys.exit(app.exec_())