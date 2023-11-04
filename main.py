from CANdapter import CANDapter, CANFrame
from fakeCANdapter import fakeCANdapter
import sched
import time
import threading
import PySimpleGUI as psg
from datetime import datetime

enable_bms = True


def crc(message):
    message.data[7] = sum(message.data[:-1]) % 256


def send_motec_keepalive(the_scheduler: sched.scheduler, candapter, frame0x100):
    the_scheduler.enter(0.048, 1, action=send_motec_keepalive, argument=(the_scheduler, candapter, frame0x100))
    candapter.send_can_message(frame0x100)


def send_packstate_2(the_scheduler: sched.scheduler, candapter, frame0x6B1: CANFrame):
    the_scheduler.enter(0.152, 1, action=send_packstate_2,
                        argument=(the_scheduler, candapter, frame0x6B1))
    if enable_bms:
        frame0x6B1.data[6] = not frame0x6B1.data[7]  # change rolling counter
        crc(frame0x6B1)
        candapter.send_can_message(frame0x6B1)


def send_cell_votages_temperatures(the_scheduler: sched.scheduler, candapter, frame0x6B3, frame0x6B4):
    the_scheduler.enter(0.056, 1, action=send_cell_votages_temperatures,
                        argument=(the_scheduler, candapter, frame0x6B3, frame0x6B4))
    if enable_bms:
        crc(frame0x6B3)
        crc(frame0x6B4)

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


def main():
    global enable_bms
    # candapter = CANDapter("/dev/ttyUSB0", 250)
    candapter = fakeCANdapter()

    motec_keepalive = 0
    high_volt = 3.8
    avg_volt = 3.6
    low_volt = 3.5
    num_cells = 30

    high_temp = 30.1
    avg_temp = 25.3
    low_temp = 20.2

    # Frames can be explained at https://docs.fsae.co.nz/en/Electrons/HV/Accumulator/BMSEmulator
    # some have been excluded since i don't think they matter (6B0, 6B2, 618)
    frame0x100 = CANFrame("100", 1, [0x00])
    # TODO: Assign this one from docs
    frame0x6B1 = CANFrame("6B1", 8, [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])  # no vars as bit 7 set in thread
    frame0x6B3 = CANFrame("6B3", 8,
                          [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, int(num_cells), 0x00])
    pack_float(high_volt, 10000, frame0x6B3, 0)
    pack_float(avg_volt, 10000, frame0x6B3, 2)
    pack_float(low_volt, 10000, frame0x6B3, 4)

    frame0x6B4 = CANFrame("6B4", 8, [0x00, 0x00, 0x00, 0x13, 0x00, 0x05, 0x00, 0x00])

    pack_float(high_temp, 1000, frame0x6B4, 0)
    pack_float(avg_temp, 1000, frame0x6B4, 2)
    pack_float(low_temp, 1000, frame0x6B4, 4)

    da_scheduler = sched.scheduler(time.monotonic, time.sleep)
    da_scheduler.enter(0.048, 1, action=send_motec_keepalive,
                       argument=(da_scheduler, candapter, frame0x100))
    da_scheduler.enter(0.152, 1, action=send_packstate_2,
                       argument=(da_scheduler, candapter, frame0x6B1))
    da_scheduler.enter(0.056, 1, action=send_cell_votages_temperatures,
                       argument=(da_scheduler, candapter, frame0x6B3, frame0x6B4))
    da_scheduler.run(blocking=False)

    # instantiate the GUI event loop thread
    # threading.Thread(target=gui_event_loop, args=()).start()

    # keep the main thread alive
    while True:
        user_input = input(
            "Enter a character (m (toggle keepalive), b (toggle bms active), h (high cell voltage fault), t): ")
        if user_input == 'm':  # motec keepalive
            print("Keepalive toggles")
            frame0x100.data[0] = not frame0x100.data[0]
            motec_keepalive = not motec_keepalive
            print(datetime.utcnow().strftime('%H:%M:%S.%f'), str(frame0x100))
        elif user_input == 'b':  # BMS active
            print("BMSActive toggles")
            enable_bms = not enable_bms
        elif user_input == 'h':  # High cell voltage
            print("High Cell Fault toggles")
            if high_volt < 4:
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
                high_temp = 51
            elif high_temp == 51:
                high_temp = 65
            else:
                high_temp = 30
            pack_float(high_temp, 1000, frame0x6B4, 0)
            print(datetime.utcnow().strftime('%H:%M:%S.%f'), str(frame0x6B4))
        else:
            print("Invalid input. Please enter m, b, v, or t.")
        print(f"m {motec_keepalive}, b {enable_bms}, h {high_volt}, l {low_volt}, c {num_cells}, t {high_temp}")


if __name__ == '__main__':
    main()
