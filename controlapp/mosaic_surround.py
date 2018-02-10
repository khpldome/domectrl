
import time
import os
import pyautogui as pag
###############################################################################
pag.FAILSAFE = False  # disables the fail-safe
###############################################################################

import domectrl.config_fds as conf
import utils.executor as ue
import xmltodict
import qweqweq.winapi_test as wt
import psutil
import pprint
from json import loads, dumps

from controlapp import app_const as c


def to_dict(input_ordered_dict):
    return loads(dumps(input_ordered_dict))


def mosaic_surround_func(action):

    str_out = ''
    dict_code = {}
    if conf.VIDEO_CARD_NAME == 'NVS 810':
        str_out, dict_code = mosaic_func(action)
    elif conf.VIDEO_CARD_NAME == 'GTX 1070':
        str_out, dict_code = surround_func(action)

    return str_out, dict_code


def get_mosaic_surround_state():

    str_out, dict_code = mosaic_func('state')
    print("dict_code", dict_code['grids'], dict_code['rows'], dict_code['cols'])

    if dict_code['grids'] == 0:
        return 'Fail'
    else:
        if dict_code['rows'] == 1 and dict_code['cols'] == 1:
            return 'False'
        else:
            return 'True'


def surround_func(action):

    str_out = ''
    dict_code = {}

    # str_out, dict_code = mosaic_func('State')
    state = get_mosaic_surround_state()
    str_out += state
    print("Start surround", state)

    if action == "Start":
        if state == 'False':
            pag.keyDown('ctrl')
            pag.keyDown('shift')
            pag.keyDown('alt')
            pag.keyDown('m')
            time.sleep(0.1)
            pag.keyUp('m')
            pag.keyUp('alt')
            pag.keyUp('shift')
            pag.keyUp('ctrl')

    elif action == "Stop":
        if state == 'True':
            pag.keyDown('ctrl')
            pag.keyDown('shift')
            pag.keyDown('alt')
            pag.keyDown('m')
            time.sleep(0.1)
            pag.keyUp('m')
            pag.keyUp('alt')
            pag.keyUp('shift')
            pag.keyUp('ctrl')

    elif action == "State":
        print("State mosaic")

    return str_out, dict_code


def mosaic_func(action):

    configureMosaic_exe = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + r'\exec\Mosaic\configureMosaic-32bit-64bit.exe '

    str_param = ''
    str_out = ''
    xml_out = ''
    dict_code = {}
    if action == "start":
        print("Start mosaic")
        # str_param = 'set cols=1 rows=2 res=1280,720,60 out=0,0 out=0,1'
        str_param = 'set cols=2 rows=4 res=1280,768,60 out=0,0 out=0,1 out=0,2 out=0,3 out=1,0 out=1,1 out=1,2 out=1,3'
        # str_param = 'set rows=1 cols=7 res=1280,768,60 out=0,0 out=0,1 out=0,2 out=0,3 out=1,0 out=1,1 out=1,2'
        # output_dict = ue.execute_command(configureMosaic_exe + str_param)
        # str_out += output_str_xml[1]
        # xml_out = output_str_xml[0]
        output_dict = ue.execute_command(configureMosaic_exe + str_param)
        # print('output_dict=', output_dict)
        if output_dict['code'] == c.SUCCESS:
            print('output=', output_dict['output'])
            xml_out = output_dict['output']
        else:
            print('str_err=', output_dict['str_err'])
            xml_out = output_dict['str_err']

    elif action == "stop":
        print("Stop mosaic")

        result = None
        for process in (process for process in psutil.process_iter() if process.name() == "chrome.exe"):
            result = process.kill()

        str_out += 'Stoped chrome.exe\n'
        str_out += str(result) + '\n'

        str_param = 'disable'
        output_dict = ue.execute_command(configureMosaic_exe + str_param)
        if output_dict['code'] == c.SUCCESS:
            print('output=', output_dict['output'])
            xml_out = output_dict['output']
        else:
            print('str_err=', output_dict['str_err'])
            xml_out = output_dict['str_err']

    elif action == "restart":
        print("Restart mosaic")
        # wt.Show()
        str_param = 'help'

    elif action == "state":
        print("State mosaic")
        str_param = 'query current'
        output_dict = ue.execute_command(configureMosaic_exe + str_param)
        print('output_dict=', output_dict)
        xml_out = output_dict['output']

    ####################################################################################################################

    if action == "restart":  # Temporary!
        print("mosaic help")
        str_out = xml_out

    else:
        odered_dict = xmltodict.parse(xml_out)  # Parse the read document string
        doc_dict = to_dict(odered_dict)
        pprint.pprint(doc_dict)

        if 'error' in doc_dict:
            grid_err = doc_dict['error']['#text']
            str_out += '\n' + grid_err + '\n'
            if grid_err == 'NvAPI_Mosaic_SetDisplayGrids failed: NVAPI_ERROR':
                if action == "start":
                    str_out += "EnableOneProjector"
                if action == "stop":
                    str_out += "Уже мозаика разобрана"
            if action == "start" and grid_err == 'Output index 2 on GPU 0 is out of bounds':
                str_out += "Включите проекторы"
            if action == "stop" and grid_err == 'No connected outputs found':
                str_out += "Невозможно разобрать мозаику"
        else:
            str_out += xml_out

            dict_code = {}
            if action == "state":

                grids = doc_dict['query']['grids']
                if grids is None:
                    str_out += "Projectors disabled"
                    dict_code.update({'grids': 0})
                else:
                    if isinstance(doc_dict['query']['grids']['grid'], list):
                        rows = doc_dict['query']['grids']['grid'][0]['@rows']
                        cols = doc_dict['query']['grids']['grid'][0]['@columns']
                    elif isinstance(doc_dict['query']['grids']['grid'], dict):
                        rows = doc_dict['query']['grids']['grid']['@rows']
                        cols = doc_dict['query']['grids']['grid']['@columns']

                    dict_code.update({'grids': 1})
                    dict_code.update({'rows': int(rows), 'cols': int(cols)})

                    # if rows == "1" and cols == "8":
                    #     str_out += "Mosaic enabled"
                    #     dict_code = "Mosaic enabled"
                    # elif rows == "1" and cols == "1":
                    #     str_out += "Mosaic disabled"
                    #     dict_code = "Mosaic enabled"

    return str_out, dict_code


