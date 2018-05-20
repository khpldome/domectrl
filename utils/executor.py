
import ctypes
from subprocess import check_output
import subprocess

import os
import xmltodict
import pprint

import domectrl.config_fds as conf
from controlapp import app_const as c

from json import loads, dumps

import psutil


def execute_command(str_command):

    enc = 'cp%d' % ctypes.windll.kernel32.GetOEMCP()

    output_dict = {}

    try:
        output = check_output(str_command, shell=True).decode(enc)
        output_dict.update({'code': c.SUCCESS,
                            'output': output})

    # except subprocess.SubprocessError as err:
    #     xml_out += err.output.decode(enc)

    except subprocess.CalledProcessError as err:
        str_err = err.output.decode(enc)
        output_dict.update({'code': c.ERROR,
                            'str_err': str_err})

    except subprocess.TimeoutExpired as err:
        str_err = err.output.decode(enc)
        output_dict.update({'code': c.TIMEOUT_ERR,
                            'str_err': str_err})

    return output_dict


def execute_command2(str_command):

    import subprocess

    out_dict = {}
    # process = subprocess.Popen(str_command, stdout=subprocess.PIPE, shell=False)
    process = psutil.Popen(str_command, stdout=subprocess.PIPE, shell=False)
    print(process)

    out_dict.update({'code': 0,
                     'pid': process.pid,
                     'created_at': process.create_time(),
                     })

    return out_dict


def _ffprobe_to_db(in_json):
    print(in_json)
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
            if 'codec_name' in stream:
                codec_name = stream['codec_name']
            else:
                codec_name = '-'

            if 'codec_long_name' in stream:
                codec_long_name = stream['codec_long_name']
            else:
                codec_long_name = '-'

            if 'r_frame_rate' in stream:
                r_frame_rate = _normalize_fps(stream['r_frame_rate'])
            else:
                r_frame_rate = '-'

            if 'width' in stream:
                width = stream['width']
            else:
                width = '-'

            if 'height' in stream:
                height = stream['height']
            else:
                height = '-'

            # pprint.pprint(stream)
            short_track_info_dict.update({
                'codec_name': codec_name,
                'codec_long_name': codec_long_name,
                'r_frame_rate': r_frame_rate,
                'width': width,
                'height': height})

    if 'duration' in temp_dict['format']:
        duration = _normalize_duration(temp_dict['format']['duration'])
    else:
        duration = '-'

    if 'bit_rate' in temp_dict['format']:
        bit_rate = _normalize_bit_rate(temp_dict['format']['bit_rate'])
    else:
        bit_rate = '-'

    short_track_info_dict.update({
        'bit_rate': bit_rate,
        'duration': duration})

    return short_track_info_dict


def get_track_info(track_path):

    ffprobe_exe = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + r'\exec\ffmpeg\ffprobe.exe '
    ffprobe_arg = '-print_format json -show_format -show_streams '
    # track_path = r'"c:\Users\Public\Videos\Sample Videos\Wildlife.wmv"'

    arg = ffprobe_exe + ffprobe_arg + track_path
    output_dict = execute_command(arg)
    if output_dict['code'] == c.SUCCESS:
        track_info_str = _ffprobe_to_db(output_dict['output'])
        print('track_info_str=', track_info_str)
    else:
        track_info_str = 'Not video file'
    return track_info_str


def _normalize_fps(in_str):
    t = in_str.split('/')
    if len(t) >= 2 and int(t[1]) != 0:
        res = int(t[0]) / float(t[1])
        return "{:.2f}".format(res)

    return "-"


def _normalize_duration(in_str):
    import time

    return time.strftime('%H:%M:%S', time.gmtime(int(float(in_str))))


def _normalize_bit_rate(in_str):
    str_out = ''
    bit_rate_int = int(in_str)
    if bit_rate_int < 1000:
        str_out = str(bit_rate_int) + ' b/s'
    elif bit_rate_int < 1000000:
        str_out = "{:.1f}".format(bit_rate_int / 1000) + ' kb/s'
    elif bit_rate_int < 1000000000:
        str_out = "{:.2f}".format(bit_rate_int / 1000000.0) + ' Mb/s'
    return str_out


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

    # pprint.pprint(get_short_track_info(res1))

    print('_normalize_bit_rate(in_str):', _normalize_bit_rate('786'))















