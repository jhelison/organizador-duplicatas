from PyQt5 import QtCore, QtGui, QtWidgets
import os
import sys

import Ui_u_columns_dialog
import _config


class Main(QtWidgets.QDialog, Ui_u_columns_dialog.Ui_Dialog):
    def __init__(self, base_columns, database_name_):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        QtWidgets.QApplication.processEvents()
        self.database_name_ = database_name_

        self.config = _config.config()

        #Enabling drag and drop
        self.listWidget_all.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.listWidget_selected.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)

        #Populate the second list
        second_list = self.config.get_config(database_name_)
        second_list.pop(0)
        second_list = self.config.translate_column_names(second_list)
        for column in second_list:
            self.listWidget_selected.addItem(column)

        first_list = base_columns
        first_list = self.config.translate_column_names(first_list)
        self.key_column = first_list.pop(0)
        for column in first_list:
            if column not in second_list:
                self.listWidget_all.addItem(column)

        self.pushButton_adicionar.clicked.connect(self.button_adicionar)
        self.listWidget_all.doubleClicked.connect(self.button_adicionar)

        self.pushButton_remover.clicked.connect(self.button_remover)
        self.listWidget_selected.doubleClicked.connect(self.button_remover)

        self.pushButton_cancelar.clicked.connect(self.close)

        self.pushButton_ok.clicked.connect(self.button_ok)

                #Enabling Multselection
        self.listWidget_all.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.listWidget_selected.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

    def button_adicionar(self):
        indexs = []
        for index in self.listWidget_all.selectedIndexes():
            indexs.append(index.row())

        for index in reversed(indexs):
            self.listWidget_selected.addItem(self.listWidget_all.item(index).text())
            self.listWidget_all.takeItem(index)

    def button_remover(self):
        indexs = []
        for index in self.listWidget_selected.selectedIndexes():
            indexs.append(index.row())
        
        for index in reversed(indexs):
            self.listWidget_all.addItem(self.listWidget_selected.item(index).text())
            self.listWidget_selected.takeItem(index)
        
    def button_ok(self):
        items_text_list = []
        items_text_list.append(self.key_column)
        for index in range(self.listWidget_selected.count()):
            items_text_list.append(self.listWidget_selected.item(index).text())

        items_text_list = self.config.translate_column_names(items_text_list, True)

        self.config.change_config({self.database_name_: items_text_list})

        self.close()


