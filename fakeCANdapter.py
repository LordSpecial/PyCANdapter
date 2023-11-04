from CANdapter import CANFrame


class fakeCANdapter:
    def send_can_message(self, can_frame: CANFrame):
        return
