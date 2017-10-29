import time

import serial

if __name__ == "__main__":

    ser = serial.Serial('COM2', 115200, parity=serial.PARITY_NONE)
    print(ser.name)
    print(ser.write(b'/n*pow=?#/n'))

    # s = ser.read(10)  # read up to ten bytes (timeout)

    while ser.is_open:
        line = ser.readline()  # read a '\n' terminated line
        print(line)
    time.sleep(10)
    ser.close()

    print("End")
