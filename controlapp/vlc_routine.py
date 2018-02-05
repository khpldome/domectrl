

import os
import psutil

import utils.executor as ue


import domectrl.config_fds as conf


vlc_bat = [os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + conf.VLC_RELPATH]


def vlc_func(action):

    global vlc_bat

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

            res_dict = ue.execute_command2(vlc_bat)
            # print(res_dict)
            str_out += str(res_dict['code']) + ' / ' + str(res_dict['pid'])
        else:
            str_out += ' запущен'

    if action == "Stop":
        print("Stop vlc")
        # for process in (process for process in psutil.process_iter() if process.name() == "vlc.exe"):
        for process in (process for process in psutil.process_iter() if process.name() in ['vlc.exe', 'WerFault.exe']):
            result = process.kill()
            str_out = 'Stoped ' + process.name() + ' / ' + str(process.pid)

    return str_out


if __name__ == "__main__":

    print(vlc_bat)

    vlc_func('Start')
    # vlc_func('Stop')
