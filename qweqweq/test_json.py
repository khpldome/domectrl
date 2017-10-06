# -*- coding: utf-8 -*-

import json
import pprint

import dpath as dpath

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
LOCALY = False   # False - Google Drive file location
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


# Read dict context
def read_dict_content(arg_lst):     # dpath.util.get(x, blob)
    '''If more than one leaf matches the glob, ValueError is raised. If the glob is
    not found, KeyError is raised.
    '''

    if LOCALY:
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
                    output = output + " " + str(nk)
                output = output + '}'
            if isinstance(x[k], list):
                output = output + ' [' + str(len(x[k])) + ']'
            output = output + "\n"
    else:
        out_dict = dpath.util.get(x, blob)
        # output = dpath.util.search(x, blob)
        output = json.dumps(out_dict, indent=4, sort_keys=True)

    print('-->', blob, '\n<--', output)

    return output


# Write dict context
def write_dict_content(arg_lst):

    if LOCALY:
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

    if LOCALY:
        write_dict2file_json(x)
    else:
        write_dict2gdrive_json(x)

    return output


# my_dict.pop('key', None)
# This will return my_dict[key] if key exists in the dictionary, and None otherwise.


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

    # https: // github.com / akesterson / dpath - python

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
    # print(json.dumps(x, indent=4, sort_keys=True))

    # dpath.util.new(x, 'a/b/e/f/g', "Roffle")
    # print(json.dumps(x, indent=4, sort_keys=True))

    # help(dpath.util.merge)
    dpath.util.merge(x, dict_json, flags=dpath.MERGE_TYPESAFE )
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


