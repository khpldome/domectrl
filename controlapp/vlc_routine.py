

import os
import psutil

import utils.executor as ue


import domectrl.config_fds as conf


vlc_bat = [os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + conf.VLC_RELPATH]


def vlc_func(action):

    global vlc_bat

    out_dict = {}
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
            str_out = str(res_dict['code']) + ' / ' + str(res_dict['pid'])

            out_dict.update({'code': 0,
                             'verbose': str_out})
        else:
            str_out = 'VLC is running'
            out_dict.update({'code': 1,
                             'verbose': str_out})

    if action == "Stop":
        print("Stop vlc")
        str_out = 'Already stopped.'
        # for process in (process for process in psutil.process_iter() if process.name() == "vlc.exe"):
        for process in (process for process in psutil.process_iter() if process.name() in ['vlc.exe', 'WerFault.exe']):
            result = process.kill()
            str_out = 'Stoped ' + process.name() + ' / ' + str(process.pid)
        #TODO
        out_dict.update({'code': 1,
                         'verbose': str_out})

    if action == "State":
        print("State vlc")
        str_out = ''
        # for process in (process for process in psutil.process_iter() if process.name() == 'vlc.exe'):

        for process in psutil.process_iter():

            if process.name() == 'vlc.exe':
                str_out = 'State ' + process.name() + ' is running'
                out_dict.update({'code': 0,
                                 'verbose': str_out})
                break
            else:
                out_dict.update({'code': 1,
                                 'verbose': 'State: not started'})

    return out_dict


if __name__ == "__main__":

    print(vlc_bat)

    vlc_func('Start')
    # vlc_func('Stop')
