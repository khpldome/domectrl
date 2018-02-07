

import os
import psutil

import utils.executor as ue
import domectrl.config_fds as conf
import time


def displaypro_func(action):

    out_dict = {}
    # displaypro_exe = r'c:\Program Files (x86)\Immersive Display PRO\ImmersiveDisplayPro.bat '
    displaypro_exe = [conf.DISPLAYPRO_ABSPATH]

    if action == "Start":
        print("Start displaypro")

        displaypro_is_running = False
        for process in psutil.process_iter():
            if process.name() == "ImmersiveDisplayPRO.exe":
                displaypro_is_running = True
                # time.sleep(2)
                break

        if displaypro_is_running is False:
            res_dict = ue.execute_command2(displaypro_exe)
            str_out = str(res_dict['code']) + ' / ' + str(res_dict['pid'])
            # time.sleep(2)
            out_dict.update({'code': 0,
                             'verbose': str_out})
        else:
            str_out = 'displaypro is running'
            out_dict.update({'code': 1,
                             'verbose': str_out})

    if action == "Stop":
        print("Stop displaypro")
        str_out = 'Already stopped.'

        for process in (process for process in psutil.process_iter() if process.name()== "ImmersiveDisplayPRO.exe"):
            result = process.kill()
            str_out = 'Stoped ' + process.name() + ' / ' + str(process.pid) + ' - ' + str(result)
        #TODO
        out_dict.update({'code': 1,
                         'verbose': str_out})

    return out_dict





