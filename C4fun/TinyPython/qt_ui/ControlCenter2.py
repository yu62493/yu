# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ControlCenter2.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TinyControlCenter(object):
    def setupUi(self, TinyControlCenter):
        TinyControlCenter.setObjectName("TinyControlCenter")
        TinyControlCenter.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(TinyControlCenter)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 751, 551))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_2.setGeometry(QtCore.QRect(0, 10, 651, 341))
        self.groupBox_2.setObjectName("groupBox_2")
        self.tableView = QtWidgets.QTableView(self.groupBox_2)
        self.tableView.setGeometry(QtCore.QRect(20, 90, 621, 231))
        self.tableView.setObjectName("tableView")
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit.setGeometry(QtCore.QRect(20, 60, 381, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.comboBox = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox.setGeometry(QtCore.QRect(20, 20, 69, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.btn_LoadData = QtWidgets.QPushButton(self.groupBox_2)
        self.btn_LoadData.setGeometry(QtCore.QRect(410, 60, 75, 23))
        self.btn_LoadData.setObjectName("btn_LoadData")
        self.btn_SaveCSV = QtWidgets.QPushButton(self.groupBox_2)
        self.btn_SaveCSV.setGeometry(QtCore.QRect(490, 60, 75, 23))
        self.btn_SaveCSV.setObjectName("btn_SaveCSV")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.groupBox = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox.setGeometry(QtCore.QRect(10, 20, 120, 80))
        self.groupBox.setObjectName("groupBox")
        self.LANButton = QtWidgets.QPushButton(self.groupBox)
        self.LANButton.setGeometry(QtCore.QRect(20, 20, 75, 23))
        self.LANButton.setObjectName("LANButton")
        self.WLANButton = QtWidgets.QPushButton(self.groupBox)
        self.WLANButton.setGeometry(QtCore.QRect(20, 50, 75, 23))
        self.WLANButton.setObjectName("WLANButton")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tabWidget.addTab(self.tab_3, "")
        TinyControlCenter.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(TinyControlCenter)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        TinyControlCenter.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(TinyControlCenter)
        self.statusbar.setObjectName("statusbar")
        TinyControlCenter.setStatusBar(self.statusbar)

        self.retranslateUi(TinyControlCenter)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(TinyControlCenter)

    def retranslateUi(self, TinyControlCenter):
        _translate = QtCore.QCoreApplication.translate
        TinyControlCenter.setWindowTitle(_translate("TinyControlCenter", "TinyControlCenter"))
        self.groupBox_2.setTitle(_translate("TinyControlCenter", "資料查詢"))
        self.comboBox.setItemText(0, _translate("TinyControlCenter", "ORD"))
        self.comboBox.setItemText(1, _translate("TinyControlCenter", "TQC"))
        self.comboBox.setItemText(2, _translate("TinyControlCenter", "WIP"))
        self.comboBox.setItemText(3, _translate("TinyControlCenter", "CPS"))
        self.comboBox.setItemText(4, _translate("TinyControlCenter", "CR2"))
        self.comboBox.setItemText(5, _translate("TinyControlCenter", "PAY"))
        self.btn_LoadData.setText(_translate("TinyControlCenter", "執行"))
        self.btn_SaveCSV.setText(_translate("TinyControlCenter", "存成CSV"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("TinyControlCenter", "資料檢索"))
        self.groupBox.setTitle(_translate("TinyControlCenter", "網路切換"))
        self.LANButton.setText(_translate("TinyControlCenter", "區域網路"))
        self.WLANButton.setText(_translate("TinyControlCenter", "WiFi"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("TinyControlCenter", "功能設定"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("TinyControlCenter", "網頁功能"))

