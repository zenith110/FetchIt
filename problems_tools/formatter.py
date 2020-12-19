# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'formatter.ui',
# licensing of 'formatter.ui' applies.
#
# Created: Fri Dec 18 22:19:11 2020
#      by: pyside2-uic  running on PySide2 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(520, 327)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 10, 101, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(50, 40, 101, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(50, 70, 101, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(50, 100, 101, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(50, 130, 101, 16))
        self.label_5.setObjectName("label_5")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(50, 170, 91, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.save = QtWidgets.QPushButton(self.centralwidget)
        self.save.setGeometry(QtCore.QRect(50, 220, 75, 23))
        self.save.setObjectName("save")
        self.problemName = QtWidgets.QLineEdit(self.centralwidget)
        self.problemName.setGeometry(QtCore.QRect(120, 10, 291, 20))
        self.problemName.setObjectName("problemName")
        self.termDate = QtWidgets.QLineEdit(self.centralwidget)
        self.termDate.setGeometry(QtCore.QRect(120, 40, 291, 20))
        self.termDate.setObjectName("termDate")
        self.Statement = QtWidgets.QLineEdit(self.centralwidget)
        self.Statement.setGeometry(QtCore.QRect(120, 70, 291, 20))
        self.Statement.setObjectName("Statement")
        self.Code = QtWidgets.QLineEdit(self.centralwidget)
        self.Code.setGeometry(QtCore.QRect(120, 100, 291, 20))
        self.Code.setObjectName("Code")
        self.Solution = QtWidgets.QLineEdit(self.centralwidget)
        self.Solution.setGeometry(QtCore.QRect(120, 130, 291, 20))
        self.Solution.setObjectName("Solution")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 520, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("MainWindow", "Problem name", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("MainWindow", "Term date", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("MainWindow", "Statement", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("MainWindow", "Code", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("MainWindow", "Solution", None, -1))
        self.comboBox.setItemText(0, QtWidgets.QApplication.translate("MainWindow", "dsn", None, -1))
        self.comboBox.setItemText(1, QtWidgets.QApplication.translate("MainWindow", "heaps", None, -1))
        self.comboBox.setItemText(2, QtWidgets.QApplication.translate("MainWindow", "tries", None, -1))
        self.comboBox.setItemText(3, QtWidgets.QApplication.translate("MainWindow", "binary-trees", None, -1))
        self.comboBox.setItemText(4, QtWidgets.QApplication.translate("MainWindow", "linked-lists", None, -1))
        self.comboBox.setItemText(5, QtWidgets.QApplication.translate("MainWindow", "stacks", None, -1))
        self.save.setText(QtWidgets.QApplication.translate("MainWindow", "submit", None, -1))

