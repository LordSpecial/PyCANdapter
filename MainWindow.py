import sys

from PySide6.QtCore import Signal
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
        
        self.rowDataAvailable.connect(self.add_row)

        self.ui.sendCANFrame.clicked.connect(lambda: self.canManager.handle_send_frame(self.ui))

        # Example usage:
        can_frame_example = CANFrame(15, 4, [10, 20, 30, 40])
        self.canManager.add_or_update_frame(self.ui.canTransmitTable, can_frame_example, 100)
    
    
    

    def add_row(self, data_list):
        """Utility function to add a row to the model."""
        print("penis")
        items = [QStandardItem(str(item)) for item in data_list]
        self.model.appendRow(items)
    
    def emit(self):
        data = ["sad", "asd", "dsa"]
        self.rowDataAvailable.emit(data)