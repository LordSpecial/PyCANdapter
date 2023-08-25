# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'homeWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
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
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QMainWindow,
    QSizePolicy, QStatusBar, QTabWidget, QTableView,
    QWidget)

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
        self.tabWidget.setGeometry(QRect(10, 40, 1261, 651))
        self.canAnalyser = QWidget()
        self.canAnalyser.setObjectName(u"canAnalyser")
        self.canMsgTable = QTableView(self.canAnalyser)
        self.canMsgTable.setObjectName(u"canMsgTable")
        self.canMsgTable.setGeometry(QRect(10, 10, 1241, 601))
        self.tabWidget.addTab(self.canAnalyser, "")
        self.canTransmit = QWidget()
        self.canTransmit.setObjectName(u"canTransmit")
        self.tabWidget.addTab(self.canTransmit, "")
        self.canLogger = QWidget()
        self.canLogger.setObjectName(u"canLogger")
        self.tabWidget.addTab(self.canLogger, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Moke CANDaptor", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.canAnalyser), QCoreApplication.translate("MainWindow", u"CAN Analyser", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.canTransmit), QCoreApplication.translate("MainWindow", u"CAN Transmitter", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.canLogger), QCoreApplication.translate("MainWindow", u"CAN Logging", None))
    # retranslateUi

