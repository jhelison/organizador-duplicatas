# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\Jhelison\Documents\Python\PYQT\Gerenciador de boletos\Modelos\u_tabelas_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1113, 477)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalGroupBox = QtWidgets.QGroupBox(Dialog)
        self.horizontalGroupBox.setObjectName("horizontalGroupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalGroupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.horizontalGroupBox)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.comboBox_lista_tabelas = QtWidgets.QComboBox(self.horizontalGroupBox)
        self.comboBox_lista_tabelas.setObjectName("comboBox_lista_tabelas")
        self.verticalLayout_2.addWidget(self.comboBox_lista_tabelas)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.horizontalGroupBox)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.lineEdit_filter_text = QtWidgets.QLineEdit(self.horizontalGroupBox)
        self.lineEdit_filter_text.setObjectName("lineEdit_filter_text")
        self.verticalLayout_3.addWidget(self.lineEdit_filter_text)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout.addWidget(self.horizontalGroupBox)
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.horizontalGroupBox.setTitle(_translate("Dialog", "Filtro"))
        self.label.setText(_translate("Dialog", "Colunas"))
        self.label_2.setText(_translate("Dialog", "Texto"))
