from PyQt5 import QtCore, QtGui, QtWidgets
import os
import sys

import _extractor
import _sqlite_handler

import Ui_u_carregamento_dialogUI


class Main(QtWidgets.QDialog, Ui_u_carregamento_dialogUI.Ui_Dialog):
    def __init__(self, path_, database):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.path = path_
        
        self.main_database = database
        
        self.extractor = _extractor.extractor(self.main_database)
        
        self.label_processados.setText("0")
        self.progressBar.setValue(0)
        QtWidgets.QApplication.processEvents()
        self.data = (self.extractor.get_files_list(self.path))
        self.label_total.setText(str(len(self.data)))
        self.pushButton_ok.clicked.connect(self.close)
        
        if len(self.data) == 0:
            self.progressBar.setValue(100)
        
        QtWidgets.QApplication.processEvents()
        
        self.label_total.setText(str(len(self.data)))
        
    def update(self):
        counter = 0
        for path in list(self.data.values()):
            counter += 1
            self.label_processados.setText(str(counter))
            self.extractor.process_file_on_database(path)
            self.progressBar.setValue((counter/len(self.data) * 100))            
            QtWidgets.QApplication.processEvents()

            self.textBrowser_output.setText(self.textBrowser_output.toPlainText() + path + "\n")
            self.textBrowser_output.moveCursor(QtGui.QTextCursor.End)

        self.pushButton_ok.setEnabled(True)
