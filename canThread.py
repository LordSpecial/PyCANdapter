from PySide6.QtCore import QThread, Signal
import time, random
from CANdapter import CANDapter, CANFrame

class MonitorThread(QThread):
    # Signal sent when message is received containing the message
    messageReceived = Signal(object)

    def __init__(self, canDapter: CANDapter):
        super().__init__()
        self.canDapter = canDapter
        self.running = True

    def run(self):
        while self.running:
            message = self.canDapter.read_can_message()
            self.messageReceived.emit(message)

    def stop(self):
        self.running = False