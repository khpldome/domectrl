
import time
import os
import pyautogui as pag
###############################################################################
pag.FAILSAFE = False  # disables the fail-safe
###############################################################################

import domectrl.config_fds as conf
import utils.executor as ue
import xmltodict
import pprint
from json import loads, dumps

from controlapp import app_const as c
from controlapp import auto_manager as am
from controlapp import displaypro_routine as dr


def to_dict(input_ordered_dict):
    return loads(dumps(input_ordered_dict))


def mosaic_surround_func(action):

    out_dict = {}
    if conf.VIDEO_CARD_NAME == 'NVS 810':
        out_dict = mosaic_func(action)
    elif conf.VIDEO_CARD_NAME == 'GTX 1070':
        out_dict = surround_func(action)

    return out_dict


def surround_func(action):

    out_dict = {}

    code = mosaic_func('state')['code']
    print(" mosaic_func('state')['code']", code)

    if action == "start":
        if code == c.MOSAIC_FALSE:

            out_dict = am.kill_processes(["chrome.exe", ])
            str_out = out_dict['str_out']
            out_dict = am.kill_processes(["vlc.exe", dr.PROCESS_NAME])
            str_out += out_dict['str_out']

            pag.keyDown('ctrl')
            pag.keyDown('shift')
            pag.keyDown('alt')
            pag.keyDown('m')
            time.sleep(0.1)
            pag.keyUp('m')
            pag.keyUp('alt')
            pag.keyUp('shift')
            pag.keyUp('ctrl')

            out_dict.update({'code': c.SUCCESS,
                             'verbose': str_out + "\n\nsent Surround start",
                             })
        elif code == c.MOSAIC_TRUE:
            out_dict.update({'code': c.ERROR,
                             'verbose': mosaic_func('state')['verbose'] + "\n\nSurround already started",
                             })
        elif code == c.MOSAIC_FAIL:
            out_dict.update({'code': c.ERROR,
                             'verbose': mosaic_func('state')['verbose'],
                             })

    elif action == "stop":
        if code == c.MOSAIC_TRUE:

            out_dict = am.kill_processes(["chrome.exe", ])
            str_out = out_dict['str_out']
            out_dict = am.kill_processes(["vlc.exe", dr.PROCESS_NAME])
            str_out += out_dict['str_out']

            pag.keyDown('ctrl')
            pag.keyDown('shift')
            pag.keyDown('alt')
            pag.keyDown('m')
            time.sleep(0.1)
            pag.keyUp('m')
            pag.keyUp('alt')
            pag.keyUp('shift')
            pag.keyUp('ctrl')

            out_dict.update({'code': c.SUCCESS,
                             'verbose': "sent Surround stop",
                             })
        else:
            out_dict.update({'code': c.ERROR,
                             'verbose': "Surround: already stopped.",
                             })

    elif action == "state":
        print("State mosaic")

        out_dict = mosaic_func('state')

    # out_dict.update({'code': code,
    #                  'verbose': str_context,
    #                  'proc_state': True,
    #                  'server_state': False})

    return out_dict


def mosaic_func(action):

    configureMosaic_exe = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + r'\exec\Mosaic\configureMosaic-32bit-64bit.exe '

    code = None
    str_out = ''
    xml_out = ''

    out_dict = {}

    if action == "start":
        print("Start mosaic")

        out_dict = am.kill_processes(["chrome.exe", ])
        str_out += out_dict['str_out']
        out_dict = am.kill_processes(["vlc.exe", dr.PROCESS_NAME])
        str_out += out_dict['str_out']

        str_param = 'set cols=2 rows=4 res=1280,768,60 out=0,0 out=0,1 out=0,2 out=0,3 out=1,0 out=1,1 out=1,2 out=1,3'
        output_dict = ue.execute_command(configureMosaic_exe + str_param)
        # print('output_dict=', output_dict)
        if output_dict['code'] == c.SUCCESS:
            print('output=', output_dict['output'])
            xml_out = output_dict['output']
        else:
            print('str_err=', output_dict['str_err'])
            xml_out = output_dict['str_err']

        code = output_dict['code']

    elif action == "stop":
        print("Stop mosaic")

        out_dict = am.kill_processes(["chrome.exe", ])
        str_out += out_dict['str_out']
        out_dict = am.kill_processes(["vlc.exe", dr.PROCESS_NAME])
        str_out += out_dict['str_out']

        str_param = 'disable'
        output_dict = ue.execute_command(configureMosaic_exe + str_param)
        if output_dict['code'] == c.SUCCESS:
            print('output=', output_dict['output'])
            xml_out = output_dict['output']
        else:
            print('str_err=', output_dict['str_err'])
            xml_out = output_dict['str_err']

        code = output_dict['code']

    elif action == "restart":
        print("Restart mosaic")

        str_param = 'help'

    elif action == "state":
        print("State mosaic")
        str_param = 'query current'
        output_dict = ue.execute_command(configureMosaic_exe + str_param)
        # print('output_dict=', output_dict)
        xml_out = output_dict['output']

        code = output_dict['code']

    out_dict.update({'code': code,
                     'str_out': str_out,
                     'xml_out': xml_out,
                     'action': action,
                     })

    return parse_mosaic_xml(out_dict)


####################################################################################################################
def parse_mosaic_xml(in_dict):

    out_dict = {}
    code = None
    str_context = ''
    action = in_dict['action']
    xml_out = in_dict['xml_out']

    if action == "restart":  # Temporary!
        print("mosaic help")
        str_context = xml_out

    else:
        odered_dict = xmltodict.parse(xml_out)  # Parse the read document string
        doc_dict = to_dict(odered_dict)
        pprint.pprint(doc_dict)

        if 'error' in doc_dict:
            grid_err = doc_dict['error']['#text']
            str_context += '\n' + grid_err + '\n'
            if grid_err == 'NvAPI_Mosaic_SetDisplayGrids failed: NVAPI_ERROR':
                if action == "start":
                    str_context += "EnableOneProjector"
                if action == "stop":
                    str_context += "Уже мозаика разобрана"

            # if action == "start" and grid_err == 'Output index 1 on GPU 0 is out of bounds':
            if action == "start" and 'Output index' in grid_err and 'is out of bounds' in grid_err:
                str_context += "Включите проекторы"
            if action == "stop" and grid_err == 'No connected outputs found':
                str_context += "Невозможно разобрать мозаику"
            code = -1
        else:
            str_context += xml_out

            if action == "state":
                grids = doc_dict['query']['grids']
                if grids is None:
                    str_context += "\nProjectors disabled (видеовыходы не активны) "
                    code = c.MOSAIC_FAIL
                    str_context += '\nFail'
                else:
                    rows = ''
                    cols = ''
                    if isinstance(doc_dict['query']['grids']['grid'], list):
                        rows = doc_dict['query']['grids']['grid'][0]['@rows']
                        cols = doc_dict['query']['grids']['grid'][0]['@columns']
                    elif isinstance(doc_dict['query']['grids']['grid'], dict):
                        rows = doc_dict['query']['grids']['grid']['@rows']
                        cols = doc_dict['query']['grids']['grid']['@columns']

                    if rows == '1' and cols == '1':
                        code = c.MOSAIC_FALSE
                        str_context += '\nFalse'
                    else:
                        code = c.MOSAIC_TRUE
                        str_context += '\nTrue'

    out_dict.update({'code': code,
                     'verbose': str_context,
                     # 'proc_state': True,
                     # 'server_state': False,
                     })

    return out_dict


