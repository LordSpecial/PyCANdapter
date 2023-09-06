import sys

from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QMainWindow, QHeaderView
from homeWindow import Ui_MainWindow  
from canManager import CAN_Manager


class MainWindow(QMainWindow):
    # Signals
    rowDataAvailable = Signal(list)

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.canManager = CAN_Manager(self.ui)

        # Populate the COM port dropdown on startup
        self.update_com_ports()

        self.canManager.init_can_table_model(self.ui.canAnalyseTable)
        self.canManager.init_can_table_model(self.ui.canTransmitTable)
        
        # Connect UI updating signals
        self.updateConnectionStatus(None)
        self.canManager.canDapter.connectionStatus.connect(self.updateConnectionStatus)  

        # Connect ui button signals
        self.ui.sendCANFrame.clicked.connect(lambda: self.canManager.handle_send_frame(self.ui))
        self.ui.repeatMsg.stateChanged.connect(self.toggle_period_box)
        self.ui.comReload.clicked.connect(self.update_com_ports)
        self.ui.connectBtn.clicked.connect(lambda: self.canManager.canDapter.start_can(self.ui.baudSelect.currentIndex(),self.ui.comSelect.currentText().split(" ", 1)[0])) # get the actual com port

    def toggle_period_box(self):
        if self.ui.repeatMsg.checkState() == Qt.Checked:
            self.ui.periodBox.setEnabled(True)
        else:
            self.ui.periodBox.setEnabled(False)

    def update_com_ports(self):
        # Clear existing items
        self.ui.comSelect.clear()
        # Add new items
        allPorts = self.canManager.canDapter.get_com_ports()
        filteredPorts = [port for port in allPorts if "Bluetooth" not in port]
        self.ui.comSelect.addItems(filteredPorts)

    def updateConnectionStatus(self, connectionPort):
        if connectionPort == None:
            self.ui.connectionStatus.setText('<font color="red">CANdapter NOT CONNECTED</font>')
        else:
            self.ui.connectionStatus.setText(f"CANdapter CONNECTED in {connectionPort}")

    

    
