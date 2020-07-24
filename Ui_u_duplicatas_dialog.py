# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\Jhelison\Documents\Python\PYQT\Gerenciador de boletos\Modelos\u_duplicatas_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1117, 312)
        Dialog.setWindowOpacity(1.0)
        Dialog.setSizeGripEnabled(False)
        Dialog.setModal(False)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget_duplicatas = QtWidgets.QTableWidget(Dialog)
        self.tableWidget_duplicatas.setObjectName("tableWidget_duplicatas")
        self.tableWidget_duplicatas.setColumnCount(0)
        self.tableWidget_duplicatas.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget_duplicatas)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_cancelar = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_cancelar.sizePolicy().hasHeightForWidth())
        self.pushButton_cancelar.setSizePolicy(sizePolicy)
        self.pushButton_cancelar.setCheckable(False)
        self.pushButton_cancelar.setObjectName("pushButton_cancelar")
        self.horizontalLayout.addWidget(self.pushButton_cancelar)
        self.pushButton_ok = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_ok.sizePolicy().hasHeightForWidth())
        self.pushButton_ok.setSizePolicy(sizePolicy)
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.horizontalLayout.addWidget(self.pushButton_ok)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Duplicatas"))
        self.pushButton_cancelar.setText(_translate("Dialog", "Cancelar"))
        self.pushButton_ok.setText(_translate("Dialog", "OK"))
