
import xmltodict
import pprint

from json import loads, dumps


import domectrl.config_fds as conf

from controlapp import mosaic_surround as mr
from controlapp import vlc_routine as vr
from controlapp import displaypro_routine as dr
from controlapp import winapi_routine as wr

import rs232_ctrl.main_rs232 as rs232
import time
import psutil


##################################################################################
def is_process_running(process_name):
    process_is_running = False
    for process in psutil.process_iter():
        if process.name() == process_name:
            process_is_running = True
            break
    return process_is_running


##################################################################################
def check_process_state(process_name):
    process_dict = {}
    for process in psutil.process_iter():
        if process.name() == process_name:
            process_dict.update({'name': process.name(),
                                 'pid': str(process.pid)})
            break
    return process_dict


##################################################################################
def kill_processes(process_list):
    process_dict = {}

    str_out = ''
    for process in psutil.process_iter():
        if process.name() in process_list:
            str_out += '\nKilled ' + process.name() + ' pid: ' + str(process.pid)
            process.kill()

    process_dict.update({'str_out': str_out})
    return process_dict


def base_func(action):
    str_out = ''

    if conf.SERVER_NAME == 'fds-Kharkiv':
        str_out = base_func_Kharkiv(action)
    elif conf.SERVER_NAME == 'fds-Kyiv':
        str_out = base_func_Kyiv(action)

    return str_out


def base_func_Kharkiv(action):

    str_out = ''
    if action == "start":
        print("Start")

        str_out = wr.winapi_func('EnableOneProjector')
        # ToDo Bad mode
        if str_out != "Включите проекторы":
            str_out += '\n' + mr.mosaic_surround_func('start')[0]
            # ToDo Check mosaic is ok

            str_out += '\n' + dr.displaypro_func('start')
            # time.sleep(20)

            str_out += '\n' + vr.vlc_func('start')
        else:
            str_out += '\n' + 'Повторно запустите систему'

    elif action == "stop":
        print("Stop system")
        str_out += '\n' + vr.vlc_func('stop')
        str_out += '\n' + dr.displaypro_func('stop')
        str_out += '\n' + mr.mosaic_surround_func('stop')[0]
        str_out += '\n' + wr.winapi_func('setPrimaryMonitor')

    else:
        str_out = "Base: Unknown command"

    return str_out


def base_func_Kyiv(action):

    str_out = ''
    if action == "start":
        print("Start")

        str_out += '\n Initial state= ' + mr.mosaic_surround_func('start')[0]

        for i in range(10):
            # state = mr.get_mosaic_surround_state()
            # out_dict = mr.mosaic_func('state')
            # state = out_dict['verbose']
            state = mr.mosaic_func('state')['verbose']

            if state == 'True':
                str_out += '\n' + dr.displaypro_func('start')
                str_out += '\n' + vr.vlc_func('start')
                break
            elif state == 'Fail':
                str_out += '\n' + 'Включите проекторы'
            elif state == 'False':
                str_out += '\n' + '...5sec...'
                time.sleep(5)

        str_out += '\n Result state= ' + mr.mosaic_surround_func('state')[0]

    elif action == "stop":
        print("Stop system")

        str_out += '\n' + vr.vlc_func('stop')
        str_out += '\n' + dr.displaypro_func('stop')
        str_out += '\n' + mr.mosaic_surround_func('stop')[0]
        time.sleep(5)
        str_out += '\n Result state= ' + mr.mosaic_surround_func('state')[0]

    elif action == "Projectors_ON":
        print("projector_func('ON')")
        res_dict = rs232.projector_func('ON')
        str_out += '\n' + str(res_dict) + ' len= ' + str(len(res_dict))

    elif action == "Projectors_OFF":
        print("projector_func('OFF')")
        res_dict = rs232.projector_func('OFF')
        str_out += '\n' + str(res_dict) + ' len= ' + str(len(res_dict))

    else:
        str_out = "Base: Unknown command"

    return str_out


if __name__ == "__main__":

    # res_dict = kill_processes(['chrome.exe', 'ImmersiveDisplayPro.exe', 'vlc.exe'])
    res_dict = kill_processes(['chrome.exe'])
    print(res_dict)


