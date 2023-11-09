from CANdapter import CANDapter, CANFrame
from fakeCANdapter import fakeCANdapter
import sched
import time
import threading
import PySimpleGUI as psg
from datetime import datetime

enable_bms = True


def crc(message):
    # Checksum Calculation:
    # Take the broadcast ID and add 8(the length).
    # Add bytes 0 - 6 to the value from step 1.
    # Chop off the least significant 8 bits(effectively turning it into an unsigned byte) and that will be the checksum value.
    # If the computed checksum does not equal the provided checksum, the values should be discarded.
    checksum = int(message.frame_id, 16) + len(message.data)
    checksum += sum(int(item) for item in message.data[:-1])
    checksum &= 0xFF
    return checksum


def send_motec_keepalive(candapter, frame0x100):
    candapter.send_can_message(frame0x100)


def send_packstate_2(candapter: CANDapter, frame0x6B1: CANFrame):
    frame0x6B1.data[6] = (frame0x6B1.data[6]+1) % 256  # change rolling counter
    frame0x6B1.data[7] = crc(frame0x6B1)
    if enable_bms:
        candapter.send_can_message(frame0x6B1)


def send_cell_votages_temperatures(candapter, frame0x6B3, frame0x6B4):
    if enable_bms:
        frame0x6B3.data[7] = crc(frame0x6B3)
        frame0x6B4.data[7] = crc(frame0x6B4)

        candapter.send_can_message(frame0x6B3)
        candapter.send_can_message(frame0x6B4)


def pack_float(val, multiplier, message, pos):
    val = val * multiplier
    message.data[pos] = int(val / 256)
    message.data[pos+1] = int(val) % 256


def gui_event_loop():
    layout = [[psg.Text(text='BMS Emulator',
                        font=('Arial Bold', 20),
                        size=20,
                        expand_x=True,
                        justification='center')],
              ]
    window = psg.Window('BMS Emulator', layout, size=(715, 250))
    while True:
        event, values = window.read()
        print(event, values)
        if event in (None, 'Exit'):
            break
    window.close()


def call_every(interval, func, *args):
    while True:
        start_time = time.time()
        func(*args)
        elapsed = time.time() - start_time
        time.sleep(max(0, interval - elapsed))


def do_fucking_everything(candapter, frame0x100, frame0x6B1, frame0x6B3, frame0x6B4):
    counter = 0;
    while True:
        start_time = time.time()
        counter = counter + 1

        if counter % (48 / 8) == 0:
            send_motec_keepalive(candapter, frame0x100)
        if counter % (56 / 8) == 0:
            send_cell_votages_temperatures(candapter, frame0x6B3, frame0x6B4)
        if counter % (152 / 8) == 0:
            send_packstate_2(candapter, frame0x6B1)

        elapsed = time.time() - start_time
        time.sleep(max(0, 0.007 - elapsed)) # 7 not 8 cause it takes a ms to run? idk but it's accurate


def main():
    global enable_bms
    candapter = CANDapter("COM5", 250)
    #candapter = fakeCANdapter()

    motec_keepalive = 0
    high_volt = 3.8
    avg_volt = 3.6
    low_volt = 3.5
    num_cells = 120

    high_temp = 30
    avg_temp = 25.3
    low_temp = 20.2

    # Frames can be explained at https://docs.fsae.co.nz/en/Electrons/HV/Accumulator/BMSEmulator
    # some have been excluded since i don't think they matter (6B0, 6B2, 618)
    frame0x100 = CANFrame("100", 1, [0x00])
    # TODO: Assign this one from docs
    frame0x6B1 = CANFrame("6B1", 8, [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])  # no vars as bit 7 set in thread
    frame0x6B3 = CANFrame("6B3", 8, [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, int(num_cells), 0x00])
    pack_float(high_volt, 10000, frame0x6B3, 0)
    pack_float(avg_volt, 10000, frame0x6B3, 2)
    pack_float(low_volt, 10000, frame0x6B3, 4)

    frame0x6B4 = CANFrame("6B4", 8, [0x00, 0x00, 0x00, 0x13, 0x00, 0x05, 0x00, 0x00])

    pack_float(high_temp, 1000, frame0x6B4, 0)
    pack_float(avg_temp, 1000, frame0x6B4, 2)
    pack_float(low_temp, 1000, frame0x6B4, 4)

    # threading.Thread(target=call_every, args=(0.048, send_motec_keepalive, candapter, frame0x100)).start()
    # threading.Thread(target=call_every, args=(0.152, send_packstate_2, candapter, frame0x6B1)).start()
    # threading.Thread(target=call_every, args=(0.056, send_cell_votages_temperatures, candapter, frame0x6B3, frame0x6B4)).start()
    threading.Thread(target=do_fucking_everything, args=(candapter, frame0x100, frame0x6B1, frame0x6B3, frame0x6B4)).start()

    # instantiate the GUI event loop thread
    # threading.Thread(target=gui_event_loop, args=()).start()

    # keep the main thread alive
    while True:
        user_input = input(
            "Enter a character (m (toggle keepalive), b (toggle bms active), h (high cell voltage fault), t): ")
        if user_input == 'm':  # motec keepalive
            print("Keepalive toggles")
            frame0x100.data[0] = not frame0x100.data[0]
            #pack_float(not frame0x100.data[0], 0, frame0x100, 0)
            motec_keepalive = not motec_keepalive

            print(datetime.utcnow().strftime('%H:%M:%S.%f'), str(frame0x100))
        elif user_input == 'b':  # BMS active
            print("BMSActive toggles")
            enable_bms = not enable_bms
        elif user_input == 'h':  # High cell voltage
            print("High Cell Fault toggles")
            if high_volt != 5:
                high_volt = 5
            else:
                high_volt = 3.8
            pack_float(high_volt, 10000, frame0x6B3, 0)
            print(datetime.utcnow().strftime('%H:%M:%S.%f'), str(frame0x6B3))
        elif user_input == 'l':  # low cell voltage
            print("Low Cell Fault toggles")
            if low_volt > 3.2:
                low_volt = 1
            else:
                low_volt = 3.5
            pack_float(low_volt, 10000, frame0x6B3, 4)
            print(datetime.utcnow().strftime('%H:%M:%S.%f'), str(frame0x6B3))
        elif user_input == 'c':  # number of cells
            print("Cell Num Fault toggles")
            if num_cells == 120:
                num_cells = 1
            else:
                num_cells = 120
            frame0x6B3.data[6] = num_cells
            print(datetime.utcnow().strftime('%H:%M:%S.%f'), str(frame0x6B3))
        elif user_input == 't':  # High temp
            print("High Cell Fault toggles")
            if high_temp == 30:
                high_temp = 55
            elif high_temp == 55:
                high_temp = 65
            else:
                high_temp = 30
            pack_float(high_temp, 1, frame0x6B4, 0)
            print(datetime.utcnow().strftime('%H:%M:%S.%f'), str(frame0x6B4))
        else:
            print("Invalid input. Please enter m, b, v, or t.")
        print(f"m {motec_keepalive}, b {enable_bms}, h {high_volt}, l {low_volt}, c {num_cells}, t {high_temp}")


if __name__ == '__main__':
    main()
