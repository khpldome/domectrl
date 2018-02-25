

import rs232_ctrl.main_rs232 as rs232
from controlapp import app_const as c

from multiprocessing import Process, Queue

import time
import random


import mod_wsgi

# print(mod_wsgi.multithread)


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

    if action == "start":
        print("projector_start")
        # res_dict, count_on = rs232.projector_func('ON')

        for i in range(5):
            p = Process(target=worker, args=(i, 'cmd', queue))
            p.start()
            # p.join()

    elif action == "stop":
        print("projector_stop")
        # res_dict, count_on = rs232.projector_func('OFF')

    elif action == "state":
        print("projector_state")
        # res_dict, count_on = rs232.projector_func('STATE')

        while True:
            if queue.empty():
                break

            obj += str(queue.get()) + ' '
        print('obj=', obj)


    # str_out = '\n' + str(res_dict) + ' len= ' + str(len(res_dict)) + ' count_on= ' + str(count_on)

    out_dict.update({'code': c.SUCCESS,
                     'verbose': str(obj),
                     'count_on': 11,
                     })

    return out_dict


