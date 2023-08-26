# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'homeWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy,
    QStatusBar, QTabWidget, QTableView, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1280, 720)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 10, 111, 31))
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 40, 1261, 651))
        self.canAnalyser = QWidget()
        self.canAnalyser.setObjectName(u"canAnalyser")
        self.canAnalyseTable = QTableView(self.canAnalyser)
        self.canAnalyseTable.setObjectName(u"canAnalyseTable")
        self.canAnalyseTable.setGeometry(QRect(10, 10, 1241, 601))
        self.tabWidget.addTab(self.canAnalyser, "")
        self.canTransmit = QWidget()
        self.canTransmit.setObjectName(u"canTransmit")
        self.idBox = QLineEdit(self.canTransmit)
        self.idBox.setObjectName(u"idBox")
        self.idBox.setGeometry(QRect(60, 50, 81, 24))
        self.lengthBox = QLineEdit(self.canTransmit)
        self.lengthBox.setObjectName(u"lengthBox")
        self.lengthBox.setGeometry(QRect(220, 50, 113, 24))
        self.msgBox = QLineEdit(self.canTransmit)
        self.msgBox.setObjectName(u"msgBox")
        self.msgBox.setGeometry(QRect(430, 50, 113, 24))
        self.idLabel = QLabel(self.canTransmit)
        self.idLabel.setObjectName(u"idLabel")
        self.idLabel.setGeometry(QRect(30, 50, 21, 21))
        self.lengthLabel = QLabel(self.canTransmit)
        self.lengthLabel.setObjectName(u"lengthLabel")
        self.lengthLabel.setGeometry(QRect(170, 50, 51, 21))
        self.msgLabel = QLabel(self.canTransmit)
        self.msgLabel.setObjectName(u"msgLabel")
        self.msgLabel.setGeometry(QRect(360, 50, 51, 21))
        self.RepeatLabel = QLabel(self.canTransmit)
        self.RepeatLabel.setObjectName(u"RepeatLabel")
        self.RepeatLabel.setGeometry(QRect(560, 50, 61, 21))
        self.repeatMsg = QCheckBox(self.canTransmit)
        self.repeatMsg.setObjectName(u"repeatMsg")
        self.repeatMsg.setGeometry(QRect(630, 50, 16, 22))
        self.periodBox = QLineEdit(self.canTransmit)
        self.periodBox.setObjectName(u"periodBox")
        self.periodBox.setGeometry(QRect(740, 50, 113, 24))
        self.periodLabel = QLabel(self.canTransmit)
        self.periodLabel.setObjectName(u"periodLabel")
        self.periodLabel.setGeometry(QRect(670, 50, 51, 21))
        self.periodLabel.setTextFormat(Qt.AutoText)
        self.sendCANFrame = QPushButton(self.canTransmit)
        self.sendCANFrame.setObjectName(u"sendCANFrame")
        self.sendCANFrame.setGeometry(QRect(880, 50, 241, 24))
        self.DescText = QLabel(self.canTransmit)
        self.DescText.setObjectName(u"DescText")
        self.DescText.setGeometry(QRect(20, 10, 301, 31))
        self.DescText.setTextFormat(Qt.AutoText)
        self.canTransmitTable = QTableView(self.canTransmit)
        self.canTransmitTable.setObjectName(u"canTransmitTable")
        self.canTransmitTable.setGeometry(QRect(20, 80, 1221, 531))
        self.tabWidget.addTab(self.canTransmit, "")
        self.canLogger = QWidget()
        self.canLogger.setObjectName(u"canLogger")
        self.tabWidget.addTab(self.canLogger, "")
        self.canPlayback = QWidget()
        self.canPlayback.setObjectName(u"canPlayback")
        self.tabWidget.addTab(self.canPlayback, "")
        self.settings = QWidget()
        self.settings.setObjectName(u"settings")
        self.tabWidget.addTab(self.settings, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Moke CANDaptor", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.canAnalyser), QCoreApplication.translate("MainWindow", u"CAN Analyser", None))
        self.idBox.setText("")
        self.idLabel.setText(QCoreApplication.translate("MainWindow", u"ID:", None))
        self.lengthLabel.setText(QCoreApplication.translate("MainWindow", u"Length:", None))
        self.msgLabel.setText(QCoreApplication.translate("MainWindow", u"Message:", None))
        self.RepeatLabel.setText(QCoreApplication.translate("MainWindow", u"Repeating:", None))
        self.repeatMsg.setText("")
        self.periodLabel.setText(QCoreApplication.translate("MainWindow", u"Period", None))
        self.sendCANFrame.setText(QCoreApplication.translate("MainWindow", u"Send Message", None))
        self.DescText.setText(QCoreApplication.translate("MainWindow", u"Send CAN Frame", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.canTransmit), QCoreApplication.translate("MainWindow", u"CAN Transmitter", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.canLogger), QCoreApplication.translate("MainWindow", u"CAN Logging", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.canPlayback), QCoreApplication.translate("MainWindow", u"CAN Playback", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.settings), QCoreApplication.translate("MainWindow", u"Settings", None))
    # retranslateUi

