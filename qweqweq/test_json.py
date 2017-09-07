import pprint
import json
# from json import loads, dumps

TARGET_FILE = 'd:\Surmylo\domectrl\qweqweq\config.json'


# def get_value_of_field(field):
#     return res_dict[field]

# print(get_value_of_field('units_per_em'))


def read_file_json_to_dict():

    file_obj = open(TARGET_FILE, "r")
    file_string = file_obj.read()
    file_obj.close()
    file_size = len(file_string)
    # print("file_string", file_size, file_string)
    # pprint.pprint(file_string)

    dict_of_json = None
    try:
        dict_of_json = json.loads(file_string)
        # pprint.pprint(["dict_of_json=", dict_of_json])
    except ValueError:
        pass  # invalid json
        print("ValueError!")

    return dict_of_json





