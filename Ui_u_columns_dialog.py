# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\Jhelison\Desktop\PYQT\Gerenciador de boletos\Modelos\u_columns_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(605, 506)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.listWidget_all = QtWidgets.QListWidget(Dialog)
        self.listWidget_all.setObjectName("listWidget_all")
        self.horizontalLayout.addWidget(self.listWidget_all)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton_adicionar = QtWidgets.QPushButton(Dialog)
        self.pushButton_adicionar.setObjectName("pushButton_adicionar")
        self.verticalLayout_2.addWidget(self.pushButton_adicionar)
        self.pushButton_remover = QtWidgets.QPushButton(Dialog)
        self.pushButton_remover.setObjectName("pushButton_remover")
        self.verticalLayout_2.addWidget(self.pushButton_remover)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.listWidget_selected = QtWidgets.QListWidget(Dialog)
        self.listWidget_selected.setObjectName("listWidget_selected")
        self.horizontalLayout.addWidget(self.listWidget_selected)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushButton_cancelar = QtWidgets.QPushButton(Dialog)
        self.pushButton_cancelar.setObjectName("pushButton_cancelar")
        self.horizontalLayout_2.addWidget(self.pushButton_cancelar)
        self.pushButton_ok = QtWidgets.QPushButton(Dialog)
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.horizontalLayout_2.addWidget(self.pushButton_ok)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Selecionar Colunas"))
        self.pushButton_adicionar.setText(_translate("Dialog", "Adicionar >"))
        self.pushButton_remover.setText(_translate("Dialog", "< Remover"))
        self.pushButton_cancelar.setText(_translate("Dialog", "Cancelar"))
        self.pushButton_ok.setText(_translate("Dialog", "OK"))
