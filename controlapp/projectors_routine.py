

import rs232_ctrl.main_rs232 as rs232
from controlapp import app_const as c


def projectors_func(action):

    out_dict = {}

    if action == "start":
        print("projector_start")
        res_dict = rs232.projector_func('ON')
        str_out = '\n' + str(res_dict) + ' len= ' + str(len(res_dict))

        out_dict.update({'code': c.SUCCESS,
                         'verbose': str_out})

    elif action == "stop":
        print("projector_stop")
        res_dict = rs232.projector_func('OFF')
        str_out = '\n' + str(res_dict) + ' len= ' + str(len(res_dict))

        out_dict.update({'code': c.SUCCESS,
                         'verbose': str_out})

    elif action == "state":
        print("projector_state")

        res_dict = rs232.projector_func('STATE')
        str_out = '\n' + str(res_dict) + ' len= ' + str(len(res_dict))

        out_dict.update({'code': c.SUCCESS,
                         'verbose': str_out})

    else:
        str_out = "Base: Unknown command"
        out_dict.update({'code': c.ERROR,
                         'verbose': str_out})

    return out_dict


