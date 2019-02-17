# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\DEV\projects\videocuter\video_cutter\UI_main.ui',
# licensing of 'C:\DEV\projects\videocuter\video_cutter\UI_main.ui' applies.
#
# Created: Sun Feb 17 15:26:38 2019
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(374, 259)
        MainWindow.setAcceptDrops(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setAcceptDrops(False)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.input_path = QtWidgets.QLineEdit(self.centralwidget)
        self.input_path.setMinimumSize(QtCore.QSize(0, 24))
        self.input_path.setAcceptDrops(False)
        self.input_path.setObjectName("input_path")
        self.horizontalLayout.addWidget(self.input_path)
        self.btn_in_browse = QtWidgets.QPushButton(self.centralwidget)
        self.btn_in_browse.setMinimumSize(QtCore.QSize(0, 24))
        self.btn_in_browse.setObjectName("btn_in_browse")
        self.horizontalLayout.addWidget(self.btn_in_browse)
        self.horizontalLayout.setStretch(0, 3)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.output_info = QtWidgets.QTextEdit(self.centralwidget)
        self.output_info.setAcceptDrops(False)
        self.output_info.setObjectName("output_info")
        self.verticalLayout.addWidget(self.output_info)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.output_path = QtWidgets.QLineEdit(self.centralwidget)
        self.output_path.setMinimumSize(QtCore.QSize(0, 24))
        self.output_path.setObjectName("output_path")
        self.horizontalLayout_2.addWidget(self.output_path)
        self.btn_out_browse = QtWidgets.QPushButton(self.centralwidget)
        self.btn_out_browse.setMinimumSize(QtCore.QSize(0, 24))
        self.btn_out_browse.setObjectName("btn_out_browse")
        self.horizontalLayout_2.addWidget(self.btn_out_browse)
        self.horizontalLayout_2.setStretch(0, 3)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
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
        self.input_path.setPlaceholderText(QtWidgets.QApplication.translate("MainWindow", "enter path to video", None, -1))
        self.btn_in_browse.setText(QtWidgets.QApplication.translate("MainWindow", "...", None, -1))
        self.output_path.setPlaceholderText(QtWidgets.QApplication.translate("MainWindow", "output directory", None, -1))
        self.btn_out_browse.setText(QtWidgets.QApplication.translate("MainWindow", "...", None, -1))
        self.btn_execute.setText(QtWidgets.QApplication.translate("MainWindow", "Cut video", None, -1))

