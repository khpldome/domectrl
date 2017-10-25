#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import pprint

import dpath as dpath
from dpath import path as path

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
LOCALY = True   # False - Google Drive file location
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

if LOCALY:
    # TARGET_FILE = 'd:\Surmylo\domectrl\qweqweq\config.json'
    TARGET_FILE = 'config.json'
    print('LOCALY=', LOCALY, 'TARGET_FILE=', TARGET_FILE)
else:
    import QuickPyDrive


# Reading data from local file
def read_file_json2dict():
    with open(TARGET_FILE, 'r') as f:
        data = json.load(f)
        # pprint.pprint(["data", data])
        print("read_file ", len(data))
        return data


# Reading data from Google Drive
def read_gdrive_json2dict():
    content = QuickPyDrive.getContent_byId(file_id=QuickPyDrive.file_id)
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
    # print(len(content))
    QuickPyDrive.putContent_byId(file_id=QuickPyDrive.file_id, content=content)
    return len(content)


def afilter(in_dict, target_str):
    if target_str in str(in_dict):
        return True
    return False


def top_dict_content(in_dict):

    output = ''
    list_keys = []

    if isinstance(in_dict, dict):
        for k in in_dict.keys():
            output = output + str(k)
            if isinstance(in_dict[k], dict):
                output = output + ' {'
                for nk in in_dict[k].keys():
                    output = output + " " + str(nk)
                output = output + '}'
                list_keys.append(k)
            elif isinstance(in_dict[k], list):
                output = output + ' [' + str(len(in_dict[k])) + ']'
                list_keys.append(k)
            else:
                list_keys.append(k)
            output = output + "\n"

    elif isinstance(in_dict, list):
        output = output + ' [' + str(len(in_dict)) + ']'
        list_keys.append(str(len(in_dict)))
    # output = dpath.path.paths(in_dict)

    return output, list_keys


def get_dict_content(glob, val, flag):

    if LOCALY:
        dict_json = read_file_json2dict()
    else:
        dict_json = read_gdrive_json2dict()

    list_keys = []
    if len(glob) > 0:
        try:
            out_dict = dpath.util.get(dict_json, glob)
            temp, list_keys = top_dict_content(out_dict)
            output = json.dumps(out_dict, indent=4, sort_keys=True)
        except KeyError:
            output = 'KeyError - not found'
        except ValueError:
            output = 'ValueError - more then one leaf'
    else:
        output, list_keys = top_dict_content(dict_json)

    print('/get -->', glob, val, flag, '\n<--', output)

    return output, list_keys


def search_dict_content(glob, val, flag):

    if LOCALY:
        dict_json = read_file_json2dict()
    else:
        dict_json = read_gdrive_json2dict()

    res_dict = dpath.util.search(dict_json, glob)
    output = json.dumps(res_dict, indent=4, sort_keys=True)

    print('/srch -->', glob, val, flag, '\n<--', output)

    return output


def set_dict_content(glob, val, flag):

    if LOCALY:
        dict_json = read_file_json2dict()
    else:
        dict_json = read_gdrive_json2dict()

    count = dpath.util.set(dict_json, glob, val)
    output = str(count)

    print('set -->', glob, val, flag, '\n<--', output)

    if LOCALY:
        write_dict2file_json(dict_json)
    else:
        write_dict2gdrive_json(dict_json)

    return output


def new_dict_content(glob, val, flag):

    if LOCALY:
        dict_json = read_file_json2dict()
    else:
        dict_json = read_gdrive_json2dict()

    if flag == '-l':    # create list
        output = dpath.util.new(dict_json, glob, [])
    else:
        output = dpath.util.new(dict_json, glob, val)

    print('new -->', glob, val, flag, '\n<--', output)

    if LOCALY:
        write_dict2file_json(dict_json)
    else:
        write_dict2gdrive_json(dict_json)

    return output


def delete_dict_content(glob, val, flag):

    if LOCALY:
        dict_json = read_file_json2dict()
    else:
        dict_json = read_gdrive_json2dict()

    count = dpath.util.delete(dict_json, glob)
    output = str(count)
    print('dlt -->', glob, val, flag, '\n<--', output)

    if LOCALY:
        write_dict2file_json(dict_json)
    else:
        write_dict2gdrive_json(dict_json)

    return output



# Copying data from Google Drive to local file [/pull]
def copy_gdrive_2_localFile():

    content = QuickPyDrive.getContent_byId(file_id=QuickPyDrive.file_id, cipher=QuickPyDrive.cipher)
    data = json.loads(content)
    # pprint.pprint(["data", data])

    with open(TARGET_FILE, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return str(f.name)


# Copying local file data to Google Drive file [/push]
def copy_localFile_2_gdrive():

    data = read_file_json2dict()
    len = write_dict2gdrive_json(data)
    return len


if __name__ == "__main__":

    # https://github.com/akesterson/dpath-python

    # # lst = ["hinting", "2dgg"]
    # # lst = ["mobile", "+380661395414"]
    # lst = ["mobile", ]
    # lst = []
    # print(">>>", lst, "\n<<<")
    # pprint.pprint([read_dict_content(lst)])

    import dpath.options
    # dpath.options.ALLOW_EMPTY_STRING_KEYS = True

    if LOCALY:
        dict_json = read_file_json2dict()
    else:
        dict_json = read_gdrive_json2dict()

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

    res = dpath.path.paths(x, dirs=True, leaves=False, path=[], skip=False)
    print(res)
    # x = {
    #     "a": 1,
    #     "b": 3,
    #     "c": 7
    # }

    # help(dpath.util.get)
    # out = dpath.util.get(x, '/a/b/d')

    # result = dpath.util.search(x, "a/b/[cd]")
    # print(json.dumps(result, indent=4, sort_keys=True))

    # help(dpath.util.search)
    # for y in dpath.util.search(x, "a/b/[cd]", yielded=True):
    #     print(y)

    # help(dpath.util.values)
    # out1 = dpath.util.values(x, '/a/b/d/*')
    # print(out1)

    # dpath.util.set(x, 'a/b/[cd]', 'Waffles')

    # dpath.util.new(x, 'a/b/e/f/g', "Roffle")
    # print(json.dumps(x, indent=4, sort_keys=True))

    # help(dpath.util.merge)
    # dpath.util.merge(x, dict_json, flags=dpath.MERGE_TYPESAFE)
    # print(json.dumps(x, indent=4, sort_keys=True))

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
    # out = dpath.util.get(x, '/social/0/ok')
    # print(out)



'''
/get
If more than one leaf matches the glob, ValueError is raised. If the glob is not found, KeyError is raised.
dpath.util.get(x, '/a/b/43')

/srch
result = dpath.util.search(x, "a/b/[cd]")
for x in dpath.util.search(x, "a/b/[cd]", yielded=True): print x
('a/b/c', [])
('a/b/d', ['red', 'buggy', 'bumpers'])
result = dpath.util.search(x, '**', afilter=afilter)

/set
Given a path glob, set all existing elements in the document
to the given value. Returns the number of elements changed.
dpath.util.set(x, 'a/b/[cd]', 'Waffles')

/new
Set the element at the terminus of path to value, and create it if it does not exist 
(as opposed to 'set' that can only change existing keys). 
path will NOT be treated like a glob. If it has globbing characters in it, they will become part of the resulting keys
dpath.util.new(x, 'a/b/e/f/g', "Roffle")
dpath.util.new(x, 'a/b/e/f/h', [])
dpath.util.new(x, 'a/b/e/f/h/13', 'Wow this is a big array, it sure is lonely in here by myself')

/mrg
dpath.util.merge(x, y)


                                            /help
                                            /info
get(x, '/a/b/43')                           /get a b 43
search(x, "a/b/[cd]")                       /srch a b [cd]
search(x, "a/b/[cd]", yielded=True)         /srch a b [cd] -y
search(x, '**', afilter=afilter)            /srch ** -f
set(x, 'a/b/[cd]', 'Waffles')               /set a b [cd] Waffles
new(x, 'a/b/e/f/g', "Roffle")               /new a b e f g Roffle
new(x, 'a/b/e/f/h', [])                     /new a b e f h -l
new(x, 'a/b/e/f/h/13', 'big array')         /new a b e f h 13 big_sarray

dlt(x, '/a/b/43')                           /dlt a b 43
                           


'''


