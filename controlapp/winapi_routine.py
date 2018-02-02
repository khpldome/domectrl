

import qweqweq.winapi_test as wt



def winapi_func(action):

    str_out = ''
    if action == "setPrimaryMonitor":
        str_out += wt.enableLG()
    elif action == "EnableOneProjector":
        res = wt.enableOneProjector()
        # ToDo Bad mode
        if res[1] == -2:
            str_out += "Включите проекторы"
        else:
            res = wt.enableOneProjector()
            str_out += str(res)
    elif action == "WinapiInfo":
        str_out += wt.winApiInfo()
    else:
        str_out += "WinAPI: Unnoun command"

    return str_out



