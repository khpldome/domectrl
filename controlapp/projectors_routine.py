

import rs232_ctrl.main_rs232 as rs232
from controlapp import app_const as c


def projectors_func(action):

    out_dict = {}

    if action == "switch_on":
        print("projector_func('ON')")
        res_dict = rs232.projector_func('ON')
        str_out = '\n' + str(res_dict) + ' len= ' + str(len(res_dict))

        out_dict.update({'code': c.SUCCESS,
                         'verbose': str_out})

    elif action == "switch_off":
        print("projector_func('OFF')")
        res_dict = rs232.projector_func('OFF')
        str_out = '\n' + str(res_dict) + ' len= ' + str(len(res_dict))

        out_dict.update({'code': c.SUCCESS,
                         'verbose': str_out})

    elif action == "state":
        print("projector_func('state')")
        str_out = 'Not emplemented yet.'
        out_dict.update({'code': c.SUCCESS,
                         'verbose': str_out})

    else:
        str_out = "Base: Unknown command"
        out_dict.update({'code': c.ERROR,
                         'verbose': str_out})

    return out_dict


