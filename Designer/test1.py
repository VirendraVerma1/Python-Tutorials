from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('test1.ui', self)
        self.h.setText("Helloworld")
        self.b1.clicked.connect(self.on_click)
        self.show()
        
    def on_click(self):
        name=self.e.text()
        print(name)
        self.h.setText(name)

if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.show()
    sys.exit(app.exec_())
