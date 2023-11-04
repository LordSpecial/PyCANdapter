from CANdapter import CANDapter, CANFrame
import threading
import time

def crc(message):
    message.data[7] = sum(message.data[:-1]) % 256

def call_every(interval, func, *args):
    while True:
        start_time = time.time()
        func(*args)
        elapsed = time.time() - start_time
        time.sleep(max(0, interval - elapsed))


def call_constantly(func, *args):
    while True:
        func(*args)


def send_motec_keepalive(candapter, frame0x100):
    candapter.send_can_message(frame0x100)


def send_packstate_2(candapter: CANDapter, bms_active, frame0x6B1: CANFrame):
    frame0x6B1.data[6] = not frame0x6B1.data[7]  # change rolling counter
    crc(frame0x6B1)
    if bms_active:
        candapter.send_can_message(frame0x6B1)


def send_cell_votages_temperatures(candapter, bms_active, frame0x6B3, frame0x6B4):
    crc(frame0x6B3)
    crc(frame0x6B4)

    if bms_active:
        candapter.send_can_message(frame0x6B3)
        candapter.send_can_message(frame0x6B4)


def handle_received_message(candapter):
    candapter.read_can_message()


def main():
    candapter = CANDapter("/dev/ttyUSB0", 250)

    # defines
    bms_active = [0]
    motec_keepalive = 0
    high_volt = 3.8
    low_volt = 3.5
    num_cells = 30
    high_temp = 30

    # Frames can be explained at https://docs.fsae.co.nz/en/Electrons/HV/Accumulator/BMSEmulator
    # some have been excluded since i don't think they matter (6B0, 6B2, 618)
    frame0x100 = CANFrame("100", 1, [0])
    frame0x6B1 = CANFrame("6B1", 8, [0xFF, 0xFF, 0xFF, 0xFF, 0x0, 0x0, 0x1, 0x0])  # no vars as bit 7 set in thread
    # TODO: check if CAN is big or little endian
    frame0x6B3 = CANFrame("6B3", 8, [0x00, int(high_volt * 1000), 0x00, 0xFF, 0x00, int(low_volt * 1000), int(num_cells), 0x0])
    frame0x6B4 = CANFrame("6B4", 8, [0x00, int(high_temp), 0x00, 0x13, 0x00, 0x05, 0x0, 0x0])

    threading.Thread(target=call_every, args=(0.048, send_motec_keepalive, candapter, frame0x100)).start()
    threading.Thread(target=call_every, args=(0.152, send_packstate_2, candapter, bms_active, frame0x6B1)).start()
    threading.Thread(target=call_every, args=(0.056, send_cell_votages_temperatures, candapter, bms_active, frame0x6B3, frame0x6B4)).start()

    # keep the main thread alive
    while True:
        user_input = input("Enter a character (m, b, v, t): ")
        if user_input == 'm':  # motec keepalive
            print("Keepalive toggles")
            frame0x100.data[0] = not frame0x100.data[0]
            motec_keepalive = not motec_keepalive
        elif user_input == 'b':  # BMS active
            print("BMSActive toggles")
            bms_active[0] = not bms_active[0]
        elif user_input == 'h':  # High cell voltage
            print("High Cell Fault toggles")
            if high_volt < 4:
                high_volt = 5
            else:
                high_volt = 3.8
        elif user_input == 'l':  # low cell voltage
            print("Low Cell Fault toggles")
            if low_volt > 3.2:
                low_volt = 1
            else:
                low_volt = 3.5
        elif user_input == 'c':  # number of cells
            print("Cell Num Fault toggles")
            if num_cells == 120:
                num_cells = 1
            else:
                num_cells = 120
        elif user_input == 't':  # High temp
            print("High Cell Fault toggles")
            if high_temp == 30:
                high_temp = 51
            elif high_temp == 51:
                high_temp = 66
            else:
                high_temp = 30
        else:
            print("Invalid input. Please enter m, b, v, or t.")
        print(f"m {motec_keepalive}, b {bms_active}, h {high_volt}, l {low_volt}, c {num_cells}, t {high_temp}")

if __name__ == '__main__':
    main()