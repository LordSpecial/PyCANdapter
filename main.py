from CANdapter import CANDapter, CANFrame


def main():
    can_dapter = CANDapter(port="COM3")

    can_dapter.close_channel()
    can_dapter.set_bitrate(500)
    can_dapter.open_channel()

    msg = CANFrame(100, 4, [10, 10, 10, 10])
    can_dapter.send_can_message(msg)

    while True:
        print(can_dapter.read_can_message())


if __name__ == '__main__':
    main()
