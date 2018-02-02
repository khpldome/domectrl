
import xmltodict
import pprint

from json import loads, dumps


import domectrl.config_fds as conf

from controlapp import mosaic_surround as mr
from controlapp import vlc_routine as vr
from controlapp import displaypro_routine as dr
from controlapp import winapi_routine as wr

import rs232_ctrl.main_rs232 as rs232


def base_func(action):
    str_out = ''

    if conf.SERVER_NAME == 'fds-Kharkiv':
        str_out = base_func_Kharkiv(action)
    elif conf.SERVER_NAME == 'fds-Kyiv':
        str_out = base_func_Kyiv(action)

    return str_out


def base_func_Kharkiv(action):

    str_out = ''
    if action == "Start":
        print("Start")

        str_out = wr.winapi_func('EnableOneProjector')
        # ToDo Bad mode
        if str_out != "Включите проекторы":
            str_out += '\n' + mr.mosaic_surround_func('Start')[0]
            # ToDo Check mosaic is ok

            str_out += '\n' + dr.displaypro_func('Start')
            # time.sleep(20)

            str_out += '\n' + vr.vlc_func('Start')
        else:
            str_out += '\n' + 'Повторно запустите систему'

    elif action == "Stop":
        print("Stop system")
        str_out += '\n' + vr.vlc_func('Stop')
        str_out += '\n' + dr.displaypro_func('Stop')
        str_out += '\n' + mr.mosaic_surround_func('Stop')[0]
        str_out += '\n' + wr.winapi_func('setPrimaryMonitor')

    else:
        str_out = "Base: Unknown command"

    return str_out


def base_func_Kyiv(action):

    str_out = ''
    if action == "Start":
        print("Start")

        str_out += '\n Initial state= ' + mr.mosaic_surround_func('Start')[0]

        for i in range(10):
            state = mr.get_mosaic_surround_state()
            if state == 'True':
                str_out += '\n' + dr.displaypro_func('Start')
                str_out += '\n' + vr.vlc_func('Start')
                break
            elif state == 'Fail':
                str_out += '\n' + 'Включите проекторы'
            elif state == 'False':
                str_out += '\n' + '...5sec...'
                time.sleep(5)

        str_out += '\n Result state= ' + mr.mosaic_surround_func('State')[0]

    elif action == "Stop":
        print("Stop system")

        str_out += '\n' + vr.vlc_func('Stop')
        str_out += '\n' + dr.displaypro_func('Stop')
        str_out += '\n' + mr.mosaic_surround_func('Stop')[0]
        time.sleep(5)
        str_out += '\n Result state= ' + mr.mosaic_surround_func('State')[0]

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







