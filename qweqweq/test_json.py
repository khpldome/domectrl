# -*- coding: utf-8 -*-

import json
import pprint

import dpath as dpath

TARGET_FILE = 'd:\Surmylo\domectrl\qweqweq\config.json'
# TARGET_FILE = 'd:\Surmylo\domectrl\qweqweq\temp.json'


# Reading data back
def read_file_json2dict():
    with open(TARGET_FILE, 'r') as f:
        data = json.load(f)
        # pprint.pprint(["data", data])
        return data


# Writing JSON data
def write_dict2file_json(data):
    with open(TARGET_FILE, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False )


# Read dict keys (3 deep)
def read_dict_content(arg_lst):
    dict_json = read_file_json2dict()
    x = {}
    dpath.util.merge(x, dict_json)

    output = "---"
    if len(arg_lst) == 0:
        output = str(l1)
    if len(arg_lst) == 3:
        output = dpath.util.search(x, "arg_lst[0]/arg_lst[1]/arg_lst[2]")
        # print(json.dumps(output, indent=4, sort_keys=True))
        # output = str(dict_json[arg_lst[0]][arg_lst[1]][arg_lst[2]]) + " &&& " + str(arg_lst[3:])
    elif len(arg_lst) == 2:
        output = dpath.util.search(x, "/" + arg_lst[0] + "/" + arg_lst[1])
        # output = str(dict_json[arg_lst[0]][arg_lst[1]]) + " &&& " + str(arg_lst[2:])
    elif len(arg_lst) == 1:
        output = dpath.util.search(x, "/" + arg_lst[0])
        output = json.dumps(output, indent=4, sort_keys=True)
        # output = str(dict_json[arg_lst[0]]) + " &&& " + str(arg_lst[1:])

    return output


if __name__ == "__main__":

    # https: // github.com / akesterson / dpath - python

    # # lst = ["hinting", "2dgg"]
    # # lst = ["mobile", "+380661395414"]
    # lst = ["mobile", ]
    # lst = []
    # print(">>>", lst, "\n<<<")
    # pprint.pprint([read_dict_content(lst)])

    import dpath.options
    # dpath.options.ALLOW_EMPTY_STRING_KEYS = True

    jd = read_file_json2dict()

    x = {
        "a": {
            "b": {
                "3": 2,
                "43": 30,
                "c": [],
                "d": ['red', 'buggy', 'bumpers'],
            }
        }
    }

    # help(dpath.util.get)
    out = dpath.util.get(x, '/a/b/d')

    # result = dpath.util.search(x, "a/b/[cd]")
    # print(json.dumps(result, indent=4, sort_keys=True))

    # help(dpath.util.search)
    # for y in dpath.util.search(x, "a/b/[cd]", yielded=True):
    #     print(y)

    # help(dpath.util.values)
    # out1 = dpath.util.values(x, '/a/b/d/*')
    # print(out1)

    # dpath.util.set(x, 'a/b/[cd]', 'Waffles')
    # print(json.dumps(x, indent=4, sort_keys=True))

    # dpath.util.new(x, 'a/b/e/f/g', "Roffle")
    # print(json.dumps(x, indent=4, sort_keys=True))

    # help(dpath.util.merge)
    dpath.util.merge(x, jd)
    print(json.dumps(x, indent=4, sort_keys=True))

    # def afilter(jd1):
    #     if "Waffles" in str(jd1):
    #         return True
    #     return False
    # result = dpath.util.search(jd, '**', afilter=afilter)
    # print(json.dumps(result, indent=4, sort_keys=True))

    # out = dpath.util.values(x, '/a/b/d/*')
    # out = dpath.util.get(x, '/skype/0/peppy6025')
    # out = dpath.util.get(x, '/deployment/0/plechan121.herokuapp.com')
    out = dpath.util.get(x, '/deployment/0/plekhanovskaya121.herokuapp.com/gmail')
    print(out)

    result = dpath.util.search(x, "deployment/0/[herokuapp]")
    print(json.dumps(result, indent=4, sort_keys=True))



