import sys

from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QMainWindow, QHeaderView
from homeWindow import Ui_MainWindow  
from canManager import CAN_Manager
from CANdapter import CANFrame

class MainWindow(QMainWindow):
    # Signals
    rowDataAvailable = Signal(list)
    rowDataAvailable = Signal(list)

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.canManager = CAN_Manager()

        self.canManager.init_can_table_model(self.ui.canAnalyseTable)
        self.canManager.init_can_table_model(self.ui.canTransmitTable)
        
        # self.rowDataAvailable.connect(self.add_row)

        self.ui.sendCANFrame.clicked.connect(lambda: self.canManager.handle_send_frame(self.ui))
        self.ui.repeatMsg.stateChanged.connect(self.toggle_period_box)

    def toggle_period_box(self, state):
        if state == Qt.Checked:
            self.ui.periodBox.setEnabled(True)
        else:
            self.ui.periodBox.setEnabled(False)

