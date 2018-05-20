

import os
import psutil

import utils.executor as ue

import domectrl.config_fds as conf
from controlapp import auto_manager as am

import requests


def check_vlc_server():

    try:
        r = requests.get('http://' + conf.HOST_IP + ':8080/requests/status.xml',
                         auth=('', '63933'))
        print("check vlc: responce=", r.status_code)
        return r.status_code
    except:
        pass


def vlc_func(action):

    import time

    out_dict = {}
    vlc_exe = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + conf.VLC_BAT_RELPATH

    if action == "start":
        # print("Start vlc=", vlc_exe)

        if os.path.exists(vlc_exe):
            print("vlc_bat exists")

        if not (os.path.isfile(vlc_exe) and os.path.exists(vlc_exe)):
            print("vlc_bat err")
            out_dict.update({'code': -1,
                             'verbose': 'vlc_bat does not exists'})
        else:

            vlc_is_running = am.is_process_running('vlc.exe')

            if vlc_is_running is False:

                res_dict = ue.execute_command2(vlc_exe)

                time.sleep(5)

                # res_dict = ue.execute_command2(
                #     [vlc_exe,
                #      # '--extraintf=http',
                #      # '--http-password=63933',
                #      # '--quiet',
                #      # '--fullscreen',
                #      # '--file-logging',
                #      # '--no-crashdump',
                #      # os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + conf.VLC_BLACK,
                #      ])
                # print(res_dict)

                str_context = 'State: ' + str(res_dict['code']) + ' is running ' + str(res_dict['pid'])
                out_dict.update({'code': 0,
                                 'verbose': str_context,
                                 'created_at': res_dict['created_at'],
                                 })
            else:
                str_out = 'VLC is running'
                if check_vlc_server() == 200:
                    str_out += ', VLC SERVER is running'
                    out_dict.update({'code': 1,
                                     'verbose': str_out})
                else:
                    str_out += ', VLC SERVER is not running'
                    out_dict.update({'code': 2,
                                     'verbose': str_out})

    if action == "stop":
        print("Stop vlc")
        str_out = 'VLC: already stopped.'
        # for process in (process for process in psutil.process_iter() if process.name() == "vlc.exe"):
        for process in (process for process in psutil.process_iter() if process.name() in ['vlc.exe', 'WerFault.exe']):
            result = process.kill()
            str_out = 'Stoped ' + process.name() + ' / ' + str(process.pid)
        #TODO
        out_dict.update({'code': 1,
                         'verbose': str_out,
                         'proc_state': False,
                         'server_state': False})

    if action == "state":
        print("State vlc")

        proc_VLC_dict = am.check_process_state('vlc.exe')
        if proc_VLC_dict:
            str_context = 'State: ' + proc_VLC_dict['name'] + ' is running ' + proc_VLC_dict['pid']

            if check_vlc_server() == 200:
                str_context += ', VLC SERVER is running'
                out_dict.update({'code': 0,
                                 'verbose': str_context,
                                 'proc_state': True,
                                 'server_state': True})
            else:
                str_context += ', VLC SERVER is not running'
                out_dict.update({'code': 2,
                                 'verbose': str_context,
                                 'proc_state': True,
                                 'server_state': False})
            out_dict.update({'created_at': proc_VLC_dict['created_at'], })
        else:
            str_context = 'State: not started'
            out_dict.update({'code': 1,
                             'verbose': str_context,
                             'proc_state': False,
                             'server_state': False})

    if action == "restart":
        print("Restart vlc")

    return out_dict


if __name__ == "__main__":

    # print(vlc_bat)
    #
    # vlc_func('start')
    # vlc_func('Stop')

    check_vlc_server()
