

import os
import psutil

import utils.executor as ue
import domectrl.config_fds as conf
import time

import pyautogui as pag
###############################################################################
pag.FAILSAFE = False  # disables the fail-safe
###############################################################################

from controlapp import auto_manager as am

# PROCESS_NAME = "ImmersiveDisplayPRO.exe"
PROCESS_NAME = "ImmersiveDisplayPro.exe"


def displaypro_func(action, param=''):

    out_dict = {}
    displaypro_exe = conf.DISPLAYPRO_ABSPATH

    if action == "start":
        print("Start displaypro")

        if os.path.exists(displaypro_exe):
            print("displaypro_exe exists")

        if not (os.path.isfile(displaypro_exe) and os.path.exists(displaypro_exe)):
            out_dict.update({'code': -1,
                             'verbose': 'displaypro_exe does not exist'})
        else:

            # displaypro_is_running = False
            # for process in psutil.process_iter():
            #     if process.name() == PROCESS_NAME:
            #         displaypro_is_running = True
            #         # time.sleep(2)
            #         break

            displaypro_is_running = am.is_process_running(PROCESS_NAME)

            if displaypro_is_running is False:
                res_dict = ue.execute_command2(displaypro_exe)
                str_out = str(res_dict['code']) + ' / ' + str(res_dict['pid'])
                # time.sleep(2)
                out_dict.update({'code': 0,
                                 'verbose': str_out,
                                 })
            else:
                str_out = 'displaypro is running'
                out_dict.update({'code': 1,
                                 'verbose': str_out})

    if action == "stop":
        print("Stop displaypro")
        str_out = 'Already stopped.'

        for process in (process for process in psutil.process_iter() if process.name() == PROCESS_NAME):
            result = process.kill()
            str_out = 'Stoped ' + process.name() + ' / ' + str(process.pid) + ' - ' + str(result)
        #TODO
        out_dict.update({'code': 1,
                         'verbose': str_out})

    if action == "state":
        print("State dpro")

        proc_dpro_dict = am.check_process_state(PROCESS_NAME)
        if proc_dpro_dict:
            str_context = 'State: ' + proc_dpro_dict['name'] + ' is running ' + proc_dpro_dict['pid']
            out_dict.update({
                'code': 1,
                'verbose': str_context,
                'proc_state': True,
                'created_at': proc_dpro_dict['created_at']
            })
        else:
            str_context = 'State: not started'
            out_dict.update({
                'code': 1,
                'verbose': str_context,
                'proc_state': False,
            })

    if action == "setconfig":

        print('http://' + conf.HOST_IP + ':6600/?' + action + '=' + param)
        # r = requests.get('http://' + conf.HOST_IP + ':8080/requests/status.xml?command=in_play&input=' + path,
        #                  auth=('', '63933'))
        # print("responce=", r)
        out_dict.update({'code': 3,
                         'verbose': ''})

    if action == "setdesktopwarping":

        print('http://' + conf.HOST_IP + ':6600/?' + action + '=' + param)
        # r = requests.get('http://' + conf.HOST_IP + ':8080/requests/status.xml?command=in_play&input=' + path,
        #                  auth=('', '63933'))
        # print("responce=", r)

        pag.keyDown('ctrl')
        pag.keyDown('shift')
        pag.keyDown('alt')
        # pag.keyDown('m')
        pag.keyDown('d')
        time.sleep(0.1)
        pag.keyUp('d')
        # pag.keyUp('m')
        pag.keyUp('alt')
        pag.keyUp('shift')
        pag.keyUp('ctrl')

        out_dict.update({'code': 4,
                         'verbose': '1234'})

    return out_dict





