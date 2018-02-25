

import rs232_ctrl.main_rs232 as rs232
from controlapp import app_const as c


def projectors_func(action):

    out_dict = {}

    if action == "start":
        print("projector_start")
        res_dict, count_on = rs232.projector_func('ON')

    elif action == "stop":
        print("projector_stop")
        res_dict, count_on = rs232.projector_func('OFF')

    elif action == "state":
        print("projector_state")
        res_dict, count_on = rs232.projector_func('STATE')

    str_out = '\n' + str(res_dict) + ' len= ' + str(len(res_dict)) + ' count_on= ' + str(count_on)

    out_dict.update({'code': c.SUCCESS,
                     'verbose': str_out,
                     'count_on': count_on,
                     })

    return out_dict


