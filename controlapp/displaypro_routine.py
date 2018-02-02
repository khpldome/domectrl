

import os
import psutil

import utils.executor as ue


def displaypro_func(action):

    displaypro_exe = r'c:\Program Files (x86)\Immersive Display PRO\ImmersiveDisplayPro.bat '

    str_out = ''
    if action == "Start":
        print("Start displaypro")

        displaypro_is_running = False
        for process in psutil.process_iter():
            if process.name() == "ImmersiveDisplayPro.exe":
                displaypro_is_running = True
                break

        if displaypro_is_running is False:
            str_param = ''
            output_str_xml = ue.execute_command1(displaypro_exe + str_param)
            str_out += output_str_xml[0]
        else:
            str_out += ""

    if action == "Stop":
        result = None
        for process in (process for process in psutil.process_iter() if process.name() == "ImmersiveDisplayPro.exe"):
            result = process.kill()

        str_out = 'Stoped ImmersiveDisplayPro.exe' + str(result)

    return str_out





