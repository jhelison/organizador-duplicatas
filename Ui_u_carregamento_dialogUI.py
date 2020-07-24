# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\Jhelison\Desktop\PYQT\Gerenciador de boletos\Modelos\u_carregamento_dialogUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(980, 279)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setProperty("value", 70)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label_processados = QtWidgets.QLabel(Dialog)
        self.label_processados.setObjectName("label_processados")
        self.horizontalLayout.addWidget(self.label_processados)
        self.label_de = QtWidgets.QLabel(Dialog)
        self.label_de.setObjectName("label_de")
        self.horizontalLayout.addWidget(self.label_de)
        self.label_total = QtWidgets.QLabel(Dialog)
        self.label_total.setObjectName("label_total")
        self.horizontalLayout.addWidget(self.label_total)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.textBrowser_output = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser_output.setObjectName("textBrowser_output")
        self.verticalLayout.addWidget(self.textBrowser_output)
        self.pushButton_ok = QtWidgets.QPushButton(Dialog)
        self.pushButton_ok.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_ok.sizePolicy().hasHeightForWidth())
        self.pushButton_ok.setSizePolicy(sizePolicy)
        self.pushButton_ok.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.verticalLayout.addWidget(self.pushButton_ok, 0, QtCore.Qt.AlignHCenter)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Processando Notas Fiscais"))
        self.label_processados.setText(_translate("Dialog", "TextLabel"))
        self.label_de.setText(_translate("Dialog", "/"))
        self.label_total.setText(_translate("Dialog", "TextLabel"))
        self.pushButton_ok.setText(_translate("Dialog", "Finalizar"))
