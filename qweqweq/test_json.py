# -*- coding: utf-8 -*-

import json
import pprint

import dpath as dpath

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
LOCAL_FILE = True   # False - Google Drive file location
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

if not LOCAL_FILE:
    import QuickPyDrive


# TARGET_FILE = 'd:\Surmylo\domectrl\qweqweq\config.json'
TARGET_FILE = 'config.json'
# TARGET_FILE = 'd:\Surmylo\domectrl\qweqweq\temp.json'
print(LOCAL_FILE, TARGET_FILE, dpath)


# Reading data from local file
def read_file_json2dict():
    with open(TARGET_FILE, 'r') as f:
        data = json.load(f)
        # pprint.pprint(["data", data])
        print("read_file ", len(data))
        return data


# Reading data from Google Drive
def read_gdrive_json2dict():
    content = QuickPyDrive.getContent_byId(file_id=QuickPyDrive.file_id, cipher=QuickPyDrive.cipher)
    data = json.loads(content)
    pprint.pprint(["data", data])
    return data


# Writing JSON data to local file
def write_dict2file_json(data):
    with open(TARGET_FILE, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# Writing JSON data to Google Drive
def write_dict2gdrive_json(data):
    content = json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False)
    print(len(content))
    QuickPyDrive.putContent_byId(file_id=QuickPyDrive.file_id, cipher=QuickPyDrive.cipher, content=content)


# Read dict context
def read_dict_content(arg_lst):

    if LOCAL_FILE:
        dict_json = read_file_json2dict()
    else:
        dict_json = read_gdrive_json2dict()

    x = {}
    dpath.util.merge(x, dict_json)

    blob = "/".join(arg_lst)
    if len(arg_lst) == 0:
        # ToDo custom output
        output = ''
        for k in x.keys():
            output = output + str(k)
            if isinstance(x[k], dict):
                output = output + ' {'
                for nk in x[k].keys():
                    output = output + str(nk)
                output = output + '}'
            if isinstance(x[k], list):
                output = output + ' [' + str(len(x[k])) + ']'
            output = output + "\n"
        # output = str(1111111122211)
    else:
        output = dpath.util.get(x, blob)
        # output = dpath.util.search(x, blob)
        output = json.dumps(output, indent=4, sort_keys=True)

    print('-->', blob, '\n<--', output)

    return output


# Write dict context
def write_dict_content(arg_lst):

    if LOCAL_FILE:
        dict_json = read_file_json2dict()
    else:
        dict_json = read_gdrive_json2dict()

    x = {}
    dpath.util.merge(x, dict_json)

    if len(arg_lst) == 0:
        # ToDo custom output
        output = str(88888887888)
    else:
        blob = "/".join(arg_lst[:-1])
        value = arg_lst[-1]
        count = dpath.util.new(x, blob, value)
        output = str(count)

    print('-->', blob, value, '\n<--', output)

    if LOCAL_FILE:
        write_dict2file_json(x)
    else:
        write_dict2gdrive_json(x)

    return output


# Copying data from Google Drive to local file [/pull]
def copy_gdrive_2_localFile():

    content = QuickPyDrive.getContent_byId(file_id=QuickPyDrive.file_id, cipher=QuickPyDrive.cipher)
    data = json.loads(content)
    pprint.pprint(["data", data])

    with open(TARGET_FILE, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return str(f.name)


# Copying local file data to Google Drive file [/push]
def copy_localFile_2_gdrive():

    data = read_file_json2dict()
    write_dict2gdrive_json(data)
    return len(data)



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
    # out = dpath.util.get(x, '/deployment/0/plekhanovskaya121.herokuapp.com/gmail')
    out = dpath.util.get(x, '/social/0/ok')
    print(out)




