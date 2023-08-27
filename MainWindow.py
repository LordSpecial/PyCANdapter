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

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.canManager = CAN_Manager()

        # Populate the COM port dropdown on startup
        self.update_com_ports()

        self.canManager.init_can_table_model(self.ui.canAnalyseTable)
        self.canManager.init_can_table_model(self.ui.canTransmitTable)
        
        # self.rowDataAvailable.connect(self.add_row)

        self.ui.sendCANFrame.clicked.connect(lambda: self.canManager.handle_send_frame(self.ui))
        self.ui.repeatMsg.stateChanged.connect(self.toggle_period_box)
        self.ui.comReload.clicked.connect(self.update_com_ports)
        self.ui.connectBtn.clicked.connect(lambda: self.canManager.canDapter.start_can(self.ui.comSelect.currentText().split(" ", 1)[0])) # get the actual com port

    def toggle_period_box(self, state):
        if state == Qt.Checked:
            self.ui.periodBox.setEnabled(True)
        else:
            self.ui.periodBox.setEnabled(False)

    def update_com_ports(self):
        # Clear existing items
        self.ui.comSelect.clear()
        # Add new items
        self.ui.comSelect.addItems(self.canManager.canDapter.get_com_ports())
    

    
