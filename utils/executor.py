
import ctypes
from subprocess import check_output
import subprocess

import os
import xmltodict
import pprint


from json import loads, dumps



def _execute_command(str_command):

    enc = 'cp%d' % ctypes.windll.kernel32.GetOEMCP()

    str_err = ''
    xml_out = ''

    try:
        xml_out += check_output(str_command, shell=True).decode(enc)

    # except subprocess.SubprocessError as err:
    #     xml_out += err.output.decode(enc)

    except subprocess.CalledProcessError as err:
        str_err += err.output.decode(enc)

    except subprocess.TimeoutExpired as err:
        str_err += err.output.decode(enc)

    return xml_out, str_err


def _ffprobe_to_db(in_json):

    temp_dict = loads(in_json)
    return dumps(temp_dict)


def get_short_track_info(json_str):

    temp_dict = {}
    short_track_info_dict = {}

    try:
        temp_dict = loads(json_str)
    except:
        print('bad json: ', json_str)
        return {}

    short_track_info_dict = {}

    for stream in temp_dict['streams']:
        if stream['codec_type'] in ('video'):
            print('&' * 50)
            # pprint.pprint(stream)
            short_track_info_dict.update({
                'codec_name': stream['codec_name'],
                'codec_long_name': stream['codec_long_name'],
                'duration': stream['duration'],
                'width': stream['width'],
                'height': stream['height']})

    short_track_info_dict.update({
        'SfOriginalFPS': temp_dict['format']['tags']['SfOriginalFPS'],
        'bit_rate': temp_dict['format']['bit_rate']})

    return short_track_info_dict


def get_track_info(track_path):

    ffprobe_exe = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + r'\exec\ffmpeg\ffprobe.exe '
    ffprobe_arg = '-print_format json -show_format -show_streams '
    # track_path = r'"c:\Users\Public\Videos\Sample Videos\Wildlife.wmv"'

    arg = ffprobe_exe + ffprobe_arg + track_path
    res1, res2 = _execute_command(arg)
    track_info_str = _ffprobe_to_db(res1)
    print('track_info_str=', track_info_str)
    return track_info_str


if __name__ == "__main__":

    ffprobe_exe = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + r'\exec\ffmpeg\ffprobe.exe '
    ffprobe_arg = '-print_format json -show_format -show_streams '
    track_path = r'"c:\Users\Public\Videos\Sample Videos\Wildlife.wmv"'

    arg = ffprobe_exe + ffprobe_arg + track_path
    # print("arg=", arg)

    res1, res2 = _execute_command(arg)
    # print("res1=", res1, "res2=", res2)

    # res_str = _ffprobe_to_db(res1)
    # print('res_str=', res_str)

    # get_track_info(track_path)

    pprint.pprint(get_short_track_info(res1))