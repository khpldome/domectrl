

import os

import domectrl.config_fds as conf



def check_fds_health():

    try:
        # r = requests.get('http://' + conf.HOST_IP + ':8080/requests/status.xml', auth=('', '63933'))
        print("responce=", r)
        # return r.status_code
    except:
        pass


def fds_func(action):

    out_dict = {}

    if action == "shutdown":
        print("shutdown...")
        os.system('shutdown -s')
        str_context = 'shutdown...'
        out_dict.update({'code': 0,
                         'verbose': str_context,
                         })

    if action == "restart":
        print("restart...")
        os.system("shutdown /r /t 1")
        str_context = 'restart...'
        out_dict.update({'code': 1,
                         'verbose': str_context,
                         })

    if action == "state":
        print("memory state")

        import psutil
        m_d = psutil.virtual_memory()
        c_d = psutil.cpu_percent()

        str_context = 'memory State...'
        str_context += '\n\n' + str(m_d)
        str_context += '\nCPU: ' + str(c_d) + '%'

        out_dict.update({'code': 1,
                         'verbose': str_context,
                         })

    return out_dict


if __name__ == "__main__":

    # print(vlc_bat)
    #
    fds_func('shutdown')
    # fds_func('Stop')

    # check_vlc_server()





















