from PySide6.QtCore import  QTimer, QElapsedTimer, Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem, QColor
from PySide6.QtWidgets import QHeaderView
from CANdapter import CANFrame, CANDapter

class CAN_Manager ():
    def __init__(self, ui) -> None:

        self.ui = ui
        self.sendQTimers = {}
        self.receiveQTimers: QElapsedTimer = {}
        
        self.canDapter = CANDapter()
        self.canDapter.messageReceived.connect(self.handle_received_message)
        
        

    def init_can_table_model(self, table):
        newModel = QStandardItemModel(1, 12)
        newModel.setHorizontalHeaderLabels(["CAN ID", "Length", "Byte 1", "Byte 2", "Byte 3", "Byte 4", "Byte 5", "Byte 6", "Byte 7", "Byte 8", "Count", "Period"])
        table.setModel(newModel)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setVisible(False)

    def add_or_update_frame(self, table, can_frame: CANFrame, highlightChanges: bool = False):
        model = table.model()

        # Check if CAN frame ID exists in the table
        for row in range(model.rowCount()):
            if model.item(row, 0) and model.item(row, 0).text() == str(can_frame.frame_id):
                # Always update the row
                for i in range(8):  # Assuming a maximum of 8 bytes for a CAN message
                    if i < len(can_frame.data):
                        if highlightChanges and model.item(row, 2 + i) and model.item(row, 2 + i).text() != str(can_frame.data[i]):
                            item = QStandardItem(str(can_frame.data[i]))
                            item.setBackground(QColor(Qt.red))
                            model.setItem(row, 2 + i, item)
                    else:
                        model.setItem(row, 2 + i, QStandardItem(""))  # Set empty string if byte data is not present

                # Update length and period
                if highlightChanges and model.item(row, 1) and model.item(row, 1).text() != str(can_frame.length):
                    item = QStandardItem(str(can_frame.length))
                    item.setBackground(QColor(Qt.red))
                    model.setItem(row, 1, item)
                    
                model.setItem(row, 11, QStandardItem(str(can_frame.period)))  # 11 is the index for the period column
    
                # Increment the counter 
                counter_item = model.item(int(row), model.columnCount() - 2)
                count = int(counter_item.text()) + 1
                counter_item.setText(str(count))
                return

        # If CAN frame ID is not found, add a new row
        items = [QStandardItem(str(can_frame.frame_id)), QStandardItem(str(can_frame.length))]
        for byte in can_frame.data:
            items.append(QStandardItem(str(byte)))
        
        while len(items) < 10:  # To match the total columns excluding period and counter
            items.append(QStandardItem(""))

        items.append(QStandardItem("1"))  # Initial count value of one
        items.append(QStandardItem(str(can_frame.period)))

        model.appendRow(items)
    
    def handle_send_frame(self, ui):
        can_frame = self.compile_frame(ui)
                
        # If the message is not repeating, send once and return
        if not ui.repeatMsg.isChecked():
            self.send_frame(can_frame)

            # Delete any old timers sending this frame
            if can_frame.frame_id in self.sendQTimers:
                self.sendQTimers[can_frame.frame_id].stop()
                del self.sendQTimers[can_frame.frame_id]
            return
        
        # If the frame is already being sent repeatedly, stop the previous timer
        if can_frame.frame_id in self.sendQTimers:
            self.sendQTimers[can_frame.frame_id].stop()

        # Make timer
        timer = QTimer()
        timer.timeout.connect(lambda: self.send_frame(self.ui, can_frame))
        timer.start(can_frame.period)

        # Save this timer, so we can manage/stop it later if needed
        self.sendQTimers[can_frame.frame_id] = timer

        ui.idBox.clear()
        ui.lengthBox.clear()
        ui.msgBox.clear()
        ui.periodBox.clear()

    def compile_frame(self, ui):
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
                transmit_period = -1

            # Split Hex into parts
            data_bytes = [int(hex_msg[i:i+2], 16) for i in range(0, len(hex_msg), 2)]
            if length != len(data_bytes):
                raise ValueError(f"Length does not match the number of bytes provided. Expected {length} bytes but found {len(data_bytes)} bytes.")

            # Create CAN Frame
            can_frame = CANFrame(frame_id, length, data_bytes, transmit_period)
        except ValueError as ve:
            print(f"Error: {ve}")

        return can_frame

    def send_frame(self, ui, can_frame):        
        self.canDapter.send_can_message(can_frame)
        self.add_or_update_frame(ui.canAnalyseTable, can_frame)
        self.add_or_update_frame(ui.canTransmitTable, can_frame, True)

    def handle_received_message(self, can_frame: CANFrame):
        if can_frame == None:
            return
        # Check if frame has a timer or not, if not make one
        if can_frame.frame_id in self.receiveQTimers:
            can_frame.period = self.receiveQTimers[can_frame.frame_id].elapsed()
        else:
            self.receiveQTimers[can_frame.frame_id] = QElapsedTimer()
            can_frame.period = -1 # set as -1 for initial value
        
        # Reset Timer
        self.receiveQTimers[can_frame.frame_id].start()
        
        # Update Analyser
        self.add_or_update_frame(self.ui.canAnalyseTable, can_frame)
