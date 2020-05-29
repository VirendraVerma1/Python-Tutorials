from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys
import test1
import os
import subprocess
import threading

def opena():
        os.system('test3.py')

        
class Ui(QtWidgets.QMainWindow):

    
        
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('test1.ui', self)
        self.h.setText("Helloworld")
        self.b1.clicked.connect(self.on_click)
        self.close.clicked.connect(self.closeapp)
        
        self.show()
        
    def on_click(self):
        name=self.e.toPlainText()
        self.h.setText(name)
        
        self.list.addItem(name)
        self.g.hide()

    def closeapp(self):
        # creating thread 
        
        t2 = threading.Thread(target=opena) 
        t2.start() 
        
        sys.exit(app.exec_())

    
        
       
        
if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.show()
    sys.exit(app.exec_())
