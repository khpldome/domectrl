

import os
import psutil

import utils.executor as ue


def vlc_func(action):

    vlc_exe = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + r'\exec\vlc-2.1.6\vlc.bat'

    str_out = ''
    if action == "Start":
        print("Start vlc")

        vlc_is_running = False
        for process in psutil.process_iter():
            if process.name() == "vlc.exe":
                vlc_is_running = True
                break

        if vlc_is_running is False:
            # str_param = '--intf=qt  --extraintf=http:rc --http-password=63933 --quiet --file-logging'
            # str_param = '--intf=qt  --extraintf=http --http-password=63933 --quiet --file-logging'
            # str_param = '--extraintf=http --http-password=63933 --quiet --qt-start-minimized'
            # str_param = '--extraintf=http --http-password=63933 --quiet'
            # без интерфейса https://wiki.videolan.org/VLC_command-line_help/
            # str_param = 'vlc -Ihttp'
            # str_param = 'vlc --intf=http'
            str_param = ''

            output_str_xml = ue.execute_command2(vlc_exe + str_param)
            str_out += output_str_xml[0]
        else:
            str_out += ''

    if action == "Stop":
        print("Stop vlc")
        # str_param = 'TASKKILL /F /IM vlc.exe'
        # str_param = 'TASKKILL /IM vlc.exe'
        # os.system(str_param)
        result = None
        for process in (process for process in psutil.process_iter() if process.name() == "vlc.exe"):
            result = process.kill()

        str_out = 'Stoped vlc.exe' + str(result)

    return str_out
