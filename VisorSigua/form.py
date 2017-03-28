# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form_v2.ui'
#
# Created: Fri Mar 17 22:52:12 2017
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!
# --------------------------------------------
# 	NOTA PARA CREAR EL ARCHIVO Y QUE COMPILE SIN PROBLEMAS
# la clave es compilar el ui con pyuic5 y cambiar
# from PyQt5 import QtCore, QtGui, QtWidgets
# por:
# from PyQt4 import QtCore, QtGui

# cambiar la linea
# self.centralwidget = QtWidgets.QtGui(MainWindow)
# por: 
# self.centralwidget = QtGui.QWidget(MainWindow)

# luego cambiar la palabra QtWidgets por QtGui en todo el documento
#------------------------------------------------------------------
from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1052, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 2)
        self.comboBox = QtGui.QComboBox(self.centralwidget)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout.addWidget(self.comboBox, 0, 2, 1, 6)
        self.pushButtonOpen = QtGui.QPushButton(self.centralwidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/img/mActionAddLayer.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonOpen.setIcon(icon)
        self.pushButtonOpen.setObjectName("pushButtonOpen")
        self.gridLayout.addWidget(self.pushButtonOpen, 0, 8, 1, 2)
        self.label_4 = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.pushButtonDeno = QtGui.QPushButton(self.centralwidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/newPrefix/img/mActionLabeling.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonDeno.setIcon(icon1)
        self.pushButtonDeno.setObjectName("pushButtonDeno")
        self.gridLayout.addWidget(self.pushButtonDeno, 1, 9, 1, 1)
        self.label_5 = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 2)
        self.pushButtonDirectorio = QtGui.QPushButton(self.centralwidget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/newPrefix/img/mActionFolder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonDirectorio.setIcon(icon2)
        self.pushButtonDirectorio.setObjectName("pushButtonDirectorio")
        self.gridLayout.addWidget(self.pushButtonDirectorio, 2, 2, 1, 2)
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout.addWidget(self.frame, 3, 0, 1, 10)
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 2, 1, 1)
        self.pushButtonUsos = QtGui.QPushButton(self.centralwidget)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/newPrefix/img/mActionAddLegend.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonUsos.setIcon(icon3)
        self.pushButtonUsos.setObjectName("pushButtonUsos")
        self.gridLayout.addWidget(self.pushButtonUsos, 1, 3, 1, 1)
        self.pushButtonDptos = QtGui.QPushButton(self.centralwidget)
        self.pushButtonDptos.setIcon(icon3)
        self.pushButtonDptos.setObjectName("pushButtonDptos")
        self.gridLayout.addWidget(self.pushButtonDptos, 1, 4, 1, 1)
        self.pushButtonCodigo = QtGui.QPushButton(self.centralwidget)
        self.pushButtonCodigo.setIcon(icon1)
        self.pushButtonCodigo.setObjectName("pushButtonCodigo")
        self.gridLayout.addWidget(self.pushButtonCodigo, 1, 8, 1, 1)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 7, 1, 1)
        self.lineEditDirectorio = QtGui.QLineEdit(self.centralwidget)
        self.lineEditDirectorio.setObjectName("lineEditDirectorio")
        self.gridLayout.addWidget(self.lineEditDirectorio, 2, 4, 1, 4)
        self.pushButtonPrint = QtGui.QPushButton(self.centralwidget)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/newPrefix/img/mActionFilePrint.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonPrint.setIcon(icon4)
        self.pushButtonPrint.setObjectName("pushButtonPrint")
        self.gridLayout.addWidget(self.pushButtonPrint, 2, 8, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1052, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Visor de edificios SIGUA"))
        self.label_3.setText(_translate("MainWindow", u"Listado edificios:"))
        self.pushButtonOpen.setText(_translate("MainWindow", u"Cargar edificio"))
        self.label_4.setText(_translate("MainWindow", u"Símbología:"))
        self.pushButtonDeno.setText(_translate("MainWindow", u"Denominación"))
        self.label_5.setText(_translate("MainWindow", u"Impresión:"))
        self.pushButtonDirectorio.setText(_translate("MainWindow", u"Directorio"))
        self.label.setText(_translate("MainWindow", u"Tema: "))
        self.pushButtonUsos.setText(_translate("MainWindow", u"Usos"))
        self.pushButtonDptos.setText(_translate("MainWindow", u"Organización"))
        self.pushButtonCodigo.setText(_translate("MainWindow", u"Código"))
        self.label_2.setText(_translate("MainWindow", u"Textos: "))
        self.pushButtonPrint.setText(_translate("MainWindow", u"Imprimir PDF"))

import recursos
