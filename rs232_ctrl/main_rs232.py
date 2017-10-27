
import datetime
import pprint
import sys

import serial
import time

import re

import multiprocessing as mp

import glob

# print(__name__)
# print('-' * 40)


# Define an output queue
output = mp.Queue()


def get_serial_ports():
    """Lists serial ports

    :raises EnvironmentError:
        On unsupported or unknown platforms
    :returns:
        A list of available serial ports
    """
    if sys.platform.startswith('win'):
        ports = ['COM' + str(i) for i in range(2, 50)]

    # elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
    #     # this is to exclude your current terminal "/dev/tty"
    #     ports = glob.glob('/dev/tty[A-Za-z]*')
    #
    #     temp_list = glob.glob ('/dev/tty[A-Za-z]*')
    #     print(temp_list)
    #     ports = []
    #     for a_port in temp_list:
    #         try:
    #             s = serial.Serial(a_port)
    #             s.close()
    #             ports.append(a_port)
    #         except serial.SerialException:
    #             pass
    #     # return ports

    # elif sys.platform.startswith('darwin'):
    #     ports = glob.glob('/dev/tty.*')

    else:
        raise EnvironmentError('Unsupported platform')

    dev_dict = {}
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            dev_dict.update({port: ['OPEN', 3, '']})
        except serial.SerialException as err:
            pass
    return dev_dict


def open_serial(dev_name):

    ser = serial.Serial()

    ser.port = dev_name
    ser.baudrate = 9600
    ser.bytesize = serial.EIGHTBITS  # number of bits per bytes
    ser.parity = serial.PARITY_NONE  # set parity check: no parity
    ser.stopbits = serial.STOPBITS_ONE  # number of stop bits

    # ser1.timeout = None                 #block read
    ser.timeout = 2  # non-block read

    ser.xonxoff = False  # disable software flow control
    ser.rtscts = False  # disable hardware (RTS/CTS) flow control
    ser.dsrdtr = False  # disable hardware (DSR/DTR) flow control

    ser.writeTimeout = 2  # timeout for write
    ser.open()
    # ser = serial.Serial(dev_name, 9600, timeout=0, parity=serial.PARITY_EVEN, rtscts=1)

    try:
        time.sleep(1)  # give the serial port sometime to receive the data
        # ser.write("\n")
        return ser

    except Exception as e:

        print("Error open serial port: " + str(e))
        return None


def close_serial(ser):
    if ser.isOpen():
        ser.close()



print("================ serial ================")

def proc_usart(shrd_serial_dev, cont, output):

    if open_serial(shrd_serial_dev):
        print("Serial port name:", shrd_serial_dev.raw)
    else:
        print("Can not open serial port")
        return

    try:
        while cont:

            str_recv = get_usart_line()
            # print ">usart", str_recv

            if str_recv:
                # result = parse_usart_position(str_recv)
                result = 1

                if result is not None:

                    # Send list to queue
                    uart_list = []
                    uart_list.append(">usart")  # id
                    uart_list.append(result)  # list of data
                    output.put(uart_list)

    except KeyboardInterrupt:

        ser.close()
        print("Ctrl+C")


def get_usart_data(ser, action):

    if ser.isOpen():

        try:
            # and discard all that is in buffer
            ser.flushInput()  # flush input buffer, discarding all its contents
            ser.flushOutput()  # flush output buffer, aborting current output

            cnt = 0
            while cnt < 2:
                cnt += 1

                # ser.write(b'\x0D*pow=?#\x0D')

                b_cmd = b'\x0D*pow=' + action.lower().encode() + b'#\x0D'
                ser.write(b_cmd)
                # ser.write(b'\x0D*ltim=?#\x0D')
                time.sleep(0.15)  # give the serial port sometime to receive the data
                response = ser.readline()

                if cnt == 2 and response:
                    str_result = ''
                    response = response.decode().strip()
                    print("response= ", response)

                    # str_re = '*POW=(.*)#'
                    # try:
                    #     res = re.search(str_re, response)
                    #     if res:
                    #         str_result = res.group(1)
                    #         print(str_result)
                    # except re.error:
                    #     str_result = response.decode().strip()
                    #     # print(re.error)

                    str_result = response

                    return str_result

        except Exception as e1:
            print("error communicating...: " + str(e1))

    else:
        print("cannot open serial port ")



def projector_func(action):

    ports_dict = get_serial_ports()
    print(ports_dict)
    state = ''
    for i in range(5):

        set_pause = False
        for port_name in ports_dict.keys():

            if (action == 'ON' and state == '*POW=ON#') or (action == 'OFF' and state == '*POW=OFF#'):
                pass
            else:
                ser = open_serial(port_name)
                if ser is not None:

                    res = get_usart_data(ser, '?')
                    ports_dict[port_name][2] = res
                    state = ports_dict[port_name][2]
                    print("Serial port name:", port_name, state)

                    if action == 'ON':
                        if state == '*POW=ON#':
                            pass
                        elif state == '*POW=OFF#' or state == '':
                            res = get_usart_data(ser, action)
                            ports_dict[port_name][2] = res
                        else:
                            set_pause = True

                    elif action == 'OFF':
                        if state == '*POW=OFF#':
                            pass
                        elif state == '*POW=ON#' or state == '':
                            res = get_usart_data(ser, action)
                            ports_dict[port_name][2] = res
                        else:
                            set_pause = True
                else:
                    print('Can not open ...')

                ser.close()

        if set_pause is True:
            set_pause = False
            time.sleep(30)

    return ports_dict


if __name__ == "__main__":

    # main_dispatcher()

    pprint.pprint(projector_func('OFF'))

    print("Bye...")

    sys.exit()


























