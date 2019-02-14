# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\DEV\projects\videocuter\video_cutter\UI_main.ui',
# licensing of 'C:\DEV\projects\videocuter\video_cutter\UI_main.ui' applies.
#
# Created: Fri Feb 15 00:26:02 2019
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(471, 325)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.input_path = QtWidgets.QLineEdit(self.centralwidget)
        self.input_path.setObjectName("input_path")
        self.horizontalLayout.addWidget(self.input_path)
        self.btn_browse = QtWidgets.QPushButton(self.centralwidget)
        self.btn_browse.setObjectName("btn_browse")
        self.horizontalLayout.addWidget(self.btn_browse)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.output_info = QtWidgets.QListWidget(self.centralwidget)
        self.output_info.setObjectName("output_info")
        self.verticalLayout.addWidget(self.output_info)
        self.btn_execute = QtWidgets.QPushButton(self.centralwidget)
        self.btn_execute.setMinimumSize(QtCore.QSize(0, 38))
        self.btn_execute.setObjectName("btn_execute")
        self.verticalLayout.addWidget(self.btn_execute)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.btn_browse.setText(QtWidgets.QApplication.translate("MainWindow", "...", None, -1))
        self.btn_execute.setText(QtWidgets.QApplication.translate("MainWindow", "PushButton", None, -1))

