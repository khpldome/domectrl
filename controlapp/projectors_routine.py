

import rs232_ctrl.main_rs232 as rs232
from controlapp import app_const as c

from multiprocessing import Process, Queue

import time
import random


import domectrl.config_fds as conf


queue = Queue()


def worker(num, cmd, q):
    """worker function"""
    # time.sleep(random.randint(5, 20))
    print('Worker', num, cmd)

    q.put(num)

    return


def projectors_func(action):

    global queue

    out_dict = {}
    obj = ' '
    res_dict = {}
    count_on = 0

    if action == "start":
        print("projector_start")
        if conf.HOSTNAME == 'fds-Kyiv':
            res_dict, count_on = rs232.projector_func('ON')

            # for i in range(5):
            #     p = Process(target=worker, args=(i, 'cmd', queue))
            #     p.start()
            #     # p.join()

    elif action == "stop":
        print("projector_stop")
        if conf.HOSTNAME == 'fds-Kyiv':
            res_dict, count_on = rs232.projector_func('OFF')

    elif action == "state":
        print("projector_state")
        if conf.HOSTNAME == 'fds-Kyiv':
            res_dict, count_on = rs232.projector_func('STATE')

            while True:
                if queue.empty():
                    break

                obj += str(queue.get()) + ' '
            print('obj=', obj)

    str_out = '\n' + str(res_dict) + ' len= ' + str(len(res_dict)) + ' count_on= ' + str(count_on)

    out_dict.update({'code': c.SUCCESS,
                     'verbose': str_out,
                     'count_on': count_on,
                     })

    return out_dict


