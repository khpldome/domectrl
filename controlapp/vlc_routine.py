

import os
import psutil

import utils.executor as ue

import domectrl.config_fds as conf
from controlapp import auto_manager as am


def vlc_func(action):

    out_dict = {}
    vlc_exe = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + conf.VLC_EXE_RELPATH
    # vlc_bat = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + VLC_BLACK

    if action == "start":
        print("Start vlc=", vlc_exe)

        if os.path.exists(vlc_exe):
            print("vlc_bat exists")

        if not (os.path.isfile(vlc_exe) and os.path.exists(vlc_exe)):
            print("vlc_bat err")
            out_dict.update({'code': -1,
                             'verbose': 'vlc_bat does not exists'})
        else:
            # vlc_is_running = False
            # for process in psutil.process_iter():
            #     if process.name() == "vlc.exe":
            #         vlc_is_running = True
            #         break

            vlc_is_running = am.is_process_running('vlc.exe')

            if vlc_is_running is False:
                # str_param = '--intf=qt  --extraintf=http:rc --http-password=63933 --quiet --file-logging'
                # str_param = '--intf=qt  --extraintf=http --http-password=63933 --quiet --file-logging'
                # str_param = '--extraintf=http --http-password=63933 --quiet --qt-start-minimized'
                # str_param = '--extraintf=http --http-password=63933 --quiet'
                # без интерфейса https://wiki.videolan.org/VLC_command-line_help/
                # str_param = 'vlc -Ihttp'
                # str_param = 'vlc --intf=http'

                # res_dict = ue.execute_command2(vlc_bat)
                res_dict = ue.execute_command2(
                    [vlc_exe,
                     '--extraintf=http',
                     '--http-password=63933',
                     '--quiet',
                     '--fullscreen',
                     '--file-logging',
                     # '--no-crashdump',
                     os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + conf.VLC_BLACK])

                # print(res_dict)
                str_out = str(res_dict['code']) + ' / ' + str(res_dict['pid'])

                out_dict.update({'code': 0,
                                 'verbose': str_out})
            else:
                str_out = 'VLC is running'
                out_dict.update({'code': 1,
                                 'verbose': str_out})

    if action == "stop":
        print("Stop vlc")
        str_out = 'Already stopped.'
        # for process in (process for process in psutil.process_iter() if process.name() == "vlc.exe"):
        for process in (process for process in psutil.process_iter() if process.name() in ['vlc.exe', 'WerFault.exe']):
            result = process.kill()
            str_out = 'Stoped ' + process.name() + ' / ' + str(process.pid)
        #TODO
        out_dict.update({'code': 1,
                         'verbose': str_out})

    if action == "state":
        print("State vlc")
        str_out = ''
        # for process in (process for process in psutil.process_iter() if process.name() == 'vlc.exe'):

        proc_VLC_dict = check_process_state('vlc.exe')
        if proc_VLC_dict:
            str_context = 'State: ' + proc_VLC_dict['name'] + ' is running ' + proc_VLC_dict['pid']
            out_dict.update({'code': 0,
                             'verbose': str_context})
        else:
            str_context = 'State: not started'
            out_dict.update({'code': 1,
                             'verbose': str_context})

        # for process in psutil.process_iter():
        #
        #     if process.name() == 'vlc.exe':
        #         str_out = 'State ' + process.name() + ' is running'
        #         out_dict.update({'code': 0,
        #                          'verbose': str_out})
        #         break
        #     else:
        #         out_dict.update({'code': 1,
        #                          'verbose': 'State: not started'})

    return out_dict


if __name__ == "__main__":

    print(vlc_bat)

    vlc_func('start')
    # vlc_func('Stop')
