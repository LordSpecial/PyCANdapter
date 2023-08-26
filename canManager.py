from PySide6.QtCore import Signal
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QMainWindow, QHeaderView
from homeWindow import Ui_MainWindow
from CANdapter import CANFrame

class CAN_Manager ():
    def __init__(self) -> None:
        pass

    def init_can_table_model(self, table):
        newModel = QStandardItemModel(5, 12)
        newModel.setHorizontalHeaderLabels(["CAN ID", "Length", "Byte 1", "Byte 2", "Byte 3", "Byte 4", "Byte 5", "Byte 6", "Byte 7", "Byte 8", "Count", "Period"])
        table.setModel(newModel)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setVisible(False)

    def add_or_update_frame(self, table, can_frame, transmit_period):
        model = table.model()

        # Try to find the row with the same frame_id
        row_to_update = -1
        for row in range(model.rowCount()):
            item = model.item(row, 0)
            if item and item.text() == str(can_frame.frame_id):
                row_to_update = row
                break

        # If found, update the count in the penultimate column
        if row_to_update != -1:
            count_item = model.item(row_to_update, 10)
            if count_item:  # check if the count_item is not None
                current_count = int(count_item.text())
                count_item.setText(str(current_count + 1))
        else:  # Else, add a new row
            items = []

            # CAN ID
            items.append(QStandardItem(str(can_frame.frame_id)))

            # Length
            items.append(QStandardItem(str(can_frame.length)))

            # Data Bytes
            for i in range(8):
                byte_value = can_frame.data[i] if i < len(can_frame.data) else ''
                items.append(QStandardItem(str(byte_value)))

            # Count (initialize to 1)
            items.append(QStandardItem("1"))

            # Period
            items.append(QStandardItem(str(transmit_period)))

            model.appendRow(items)

    
    def handle_send_frame(self, ui):
            if ui.idBox.text() == '':
                return
            try:
                frame_id = int(ui.idBox.text())
                length = int(ui.lengthBox.text())
                hex_msg = ui.msgBox.text().strip()

                # Get transmit_period only if repeatMsg is checked
                if ui.repeatMsg.isChecked():
                    transmit_period = int(ui.periodBox.text())
                else:
                    transmit_period = 'N/A'

                # Split Hex into parts
                data_bytes = [int(hex_msg[i:i+2], 16) for i in range(0, len(hex_msg), 2)]
                if length != len(data_bytes):
                    raise ValueError(f"Length does not match the number of bytes provided. Expected {length} bytes but found {len(data_bytes)} bytes.")

                can_frame = CANFrame(frame_id, length, data_bytes)

                self.add_or_update_frame(ui.canTransmitTable, can_frame, transmit_period)
                ui.idBox.clear()
                ui.lengthBox.clear()
                ui.msgBox.clear()
                ui.periodBox.clear()
            except ValueError as ve:
                print(f"Error: {ve}")
