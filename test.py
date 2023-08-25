import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTableView
from PySide6.QtGui import QStandardItem, QStandardItemModel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the QTableView and the model
        self.canMsgTable = QTableView(self)
        self.model = QStandardItemModel()
        self.canMsgTable.setModel(self.model)

        # Add some headers for demonstration purposes
        self.model.setHorizontalHeaderLabels(['Header1', 'Header2', 'Header3'])

        # Add the data row
        self.add_row(["cella123", "cellb321", "farts"])

        self.setCentralWidget(self.canMsgTable)

    def add_row(self, data):
        """Utility function to add a row to the model."""
        row_items = [QStandardItem(item) for item in data]
        self.model.appendRow(row_items)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
