import serial
import re
import threading

CR = '\015'


class CANFrame:
    def __init__(self, frame_id, length, data):
        self.frame_id = frame_id
        self.length = length
        self.data = data

    def __str__(self):
        return f'id: {self.frame_id} | length: {self.length} | data: {self.data}'

    def to_bytes(self):
        identifier = str(self.frame_id)

        if len(identifier) == 2:
            identifier = '0' + identifier
        elif len(identifier) == 1:
            identifier = '00' + identifier
        elif len(identifier) == 0:
            identifier = '000'

        length = str(self.length)
        data = b''
        for item in self.data:
            data += bytes(str(hex(item)).replace("0x",""), "ASCII")

        return bytes(identifier, 'ascii') + bytes(length, 'ascii') + data


def parse_can_frame(frame):
    the_id = int(frame[:3], 16)
    length = int(frame[3:4], 16)
    data = [int(frame[4 + i:4 + i + 2], 16) if i + 4 < len(frame) else 0 for i in range(8)]

    return the_id, length, data


def get_baud_rate_command(rate: int):
    command = b'S5'

    if rate == 10:
        command = b'S0'
    elif rate == 20:
        command = b'S1'
    elif rate == 50:
        command = b'S2'
    elif rate == 100:
        command = b'S3'
    elif rate == 125:
        command = b'S4'
    elif rate == 250:
        command = b'S5'
    elif rate == 500:
        command = b'S6'
    elif rate == 800:
        command = b'S7'
    elif rate == 1000:
        command = b'S8'

    return command


def clean_can_frame(data):
    frames = re.sub(r'[^a-zA-Z0-9]', '', data)
    frames = frames.split('t')
    frames.remove('')
    return frames


class CANDapter:
    baud_rate = 250
    serial_port = 0

    def __init__(self, port, baud_rate):
        # self.subs = subs

        self.serial_port = serial.Serial(
            port
        )

        self.send_command_with_response(b'C')  # restart candapter

        while not self.send_command_with_response(
                get_baud_rate_command(self.baud_rate)
        ):
            pass

        while not self.send_command_with_response(b'O'):  # start candapter
            pass

        self.serial_thread = threading.Thread(target=self.read_serial)
        self.serial_thread.daemon = True
        self.serial_thread.start()

    def send_command_with_response(self, command: bytes):
        # NOTE DO NOT RUN THIS IF YOU HAVE READING THREAD OPEN
        if not self.serial_port.is_open:
            return False

        msg = b'\015' + command + b'\015'
        self.serial_port.write(msg)
        response = self.serial_port.read()

        print(f'Sent cmd: {command} | Response: {response}')
        return response == b'\06'

    def send_command(self, command: bytes):
        if not self.serial_port.is_open:
            return False

        msg = b'\015' + command + b'\015'
        self.serial_port.write(msg)
        return True

    def can_send_callback(self, can_frame):
        self.send_command(
            f'T{can_frame.std_id:03X}'
            f'{len(can_frame.data):01X}'
            f'{"".join(["%02X" % byte for byte in can_frame.data])}'
            .encode())

    def read_serial(self):
        while True:
            if self.serial_port.in_waiting > 0:
                data = self.serial_port.read_until(b'\r') \
                    .decode() \
                    .strip()

                try:
                    index_of_t = data.index('t')
                    data = data[index_of_t:]
                except ValueError:
                    pass
                # TODO: implement subscribers (maybe) or just a callback here to handle message received
                # if data[0] == 't':
                #     cleaned_data_list = clean_can_frame(data)
                #     for cleaned_data in cleaned_data_list:
                #         try:
                #             frame = parse_can_frame(cleaned_data)
                #             for sub in self.subs:
                #                 sub.event.set()
                #                 sub.message = frame
                #         except:
                #             print('')

    def send_can_message(self, can_frame: CANFrame):
        command = b'T' + can_frame.to_bytes()
        self.send_command(command)

    def set_bitrate(self, rate: int) -> bool:
        """https://www.ewertenergy.com/products/candapter/downloads/candapter_manual.pdf
        set rate to one of the following:
            10 Kbit
            20 Kbit
            50 Kbit
            100 Kbit
            125 Kbit
            250 Kbit
            500 Kbit
            800 Kbit
            1 Mbit

        returns bool depending on if successfully set
        """
        if rate == 10:
            command = b'S0'
        elif rate == 20:
            command = b'S1'
        elif rate == 50:
            command = b'S2'
        elif rate == 100:
            command = b'S3'
        elif rate == 125:
            command = b'S4'
        elif rate == 250:
            command = b'S5'
        elif rate == 500:
            command = b'S6'
        elif rate == 800:
            command = b'S7'
        elif rate == 1000:
            command = b'S8'
        else:
            raise ValueError("Rate given is not available on this device")

        return self.send_command(command)

    def open_channel(self):
        return self.send_command(b'O')

    def close_channel(self):
        return self.send_command(b'C')

    def _read_until(self):
        return self.serial_port.read_until(expected=b'\r')

    def read_can_message(self):
        can_message = str(self._read_until())[3:-3]

        data = [''] * int(can_message[3])
        for idx, char in enumerate(can_message[4:]):
            idx //= 2
            data[idx] += str(char)

        return CANFrame(
            can_message[0:3],
            can_message[3],
            data
        )
