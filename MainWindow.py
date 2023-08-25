import sys

from PySide6.QtCore import Signal
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QMainWindow, QHeaderView
from homeWindow import Ui_MainWindow  

class MainWindow(QMainWindow):
    # Signals
    rowDataAvailable = Signal(list)

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        
        self.ui.canMsgTable.setModel(self.init_can_table_model())
        
        header = self.ui.canMsgTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.rowDataAvailable.connect(self.add_row)
    
    def init_can_table_model(self):
        model = QStandardItemModel(5, 3)
        model.setHorizontalHeaderLabels(["CAN ID", "Length", "Byte 1", "Byte 2", "Byte 3", "Byte 4", "Byte 5", "Byte 6", "Byte 7", "Byte 8"])
    
        return model

    def add_row(self, data_list):
        """Utility function to add a row to the model."""
        print("penis")
        items = [QStandardItem(str(item)) for item in data_list]
        self.model.appendRow(items)
    
    def emit(self):
        data = ["sad", "asd", "dsa"]
        self.rowDataAvailable.emit(data)