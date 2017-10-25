from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import View, TemplateView
import xmltodict
import pprint

import os
import psutil

import time

import qweqweq.winapi_test as wt


def index(request):
    context = {'latest_question_list': 22}
    return render(request, 'dome/index.html', context)


class MosaicActionView(TemplateView):

    template_name = 'dome/index.html'

    def get(self, request, *args, **kwargs):
        # print("get=", mosaic_action)

        # messages.error(request, 'User already has this module.')
        # return HttpResponse('Result: ' + text_output)

        return super(MosaicActionView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MosaicActionView, self).get_context_data(**kwargs)
        text_output = ""
        if 'mosaic_action' in kwargs:
            mosaic_action = kwargs['mosaic_action']
            print("mosaic_action=", mosaic_action)

            text_output = mosaic_func(mosaic_action)[0]

        if 'vlc_action' in kwargs:
            vlc_action = kwargs['vlc_action']
            print("vlc_action=", vlc_action)

            text_output = vlc_func(vlc_action)

        # context['pages'] = ModulePage.objects.filter(module_id=self.mymodule.id)
        context.update({
            "data_context": text_output,
            "revenue_shared": 22,
        })
        return context

    # def get_success_url(self):
    #     # Get clone id
    #     return reverse_lazy('monetize_module', kwargs={'module_id': module_id})


class VlcActionView(TemplateView):

    template_name = 'dome/index.html'

    def get(self, request, *args, **kwargs):
        return super(VlcActionView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(VlcActionView, self).get_context_data(**kwargs)
        text_output = ""

        if 'vlc_action' in kwargs:
            vlc_action = kwargs['vlc_action']
            print("vlc_action=", vlc_action)

            text_output = vlc_func(vlc_action)

        context['data_context'] = text_output
        return context


class WinapiActionView(TemplateView):

    template_name = 'dome/index.html'

    def get(self, request, *args, **kwargs):
        return super(WinapiActionView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(WinapiActionView, self).get_context_data(**kwargs)
        text_output = ""

        if 'winapi_action' in kwargs:
            winapi_action = kwargs['winapi_action']
            print("winapi_action=", winapi_action)

            text_output = winapi_func(winapi_action)

        context['data_context'] = text_output
        return context


class DisplayproActionView(TemplateView):

    template_name = 'dome/index.html'

    def get(self, request, *args, **kwargs):
        return super(DisplayproActionView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DisplayproActionView, self).get_context_data(**kwargs)
        text_output = ""

        if 'displaypro_action' in kwargs:
            displaypro_action = kwargs['displaypro_action']
            print("displaypro_action=", displaypro_action)

            text_output = displaypro_func(displaypro_action)

        context['data_context'] = text_output
        return context


def base_index(request):
    context = {'latest_question_list': 22}
    return render(request, 'dome/base.html', context)


class BaseView(TemplateView):

    template_name = 'dome/base.html'

    def get(self, request, *args, **kwargs):
        return super(BaseView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)
        text_output = ""

        if 'base_action' in kwargs:
            base_action = kwargs['base_action']
            print("base_action=", base_action)

            text_output = base_func(base_action)

        context['data_context'] = text_output
        return context


def _execute_command(str_command, timeout=0):

    import ctypes
    from subprocess import check_output
    import subprocess

    enc = 'cp%d' % ctypes.windll.kernel32.GetOEMCP()

    xml_out = ''
    str_out = ''
    if timeout == 0:

        try:
            xml_out += check_output(str_command, shell=True).decode(enc)
        except subprocess.CalledProcessError as err:
            # print('e.output: ', e.output)
            xml_out += err.output.decode(enc)
    else:
        try:
            xml_out += check_output(str_command, shell=True, timeout=timeout).decode(enc)
        except subprocess.CalledProcessError as err:
            # print('e.output: ', e.output)
            xml_out += err.output.decode(enc)
        except subprocess.TimeoutExpired as err:
            str_out += "timeout n sec\n"
            str_out += err.output.decode(enc)

    return str_out, xml_out


def _execute_command1(str_command, timeout=0):

    import ctypes
    from subprocess import check_output
    import subprocess

    enc = 'cp%d' % ctypes.windll.kernel32.GetOEMCP()

    args = [r'c:\Program Files (x86)\Immersive Display PRO\ImmersiveDisplayPro.bat']
    process_displayPro = subprocess.Popen(args, stdout=subprocess.PIPE, shell=False)

    xml_out = ''
    str_out = ''
    # try:
    #         xml_out += check_output(str_command, shell=True).decode(enc)
    # except subprocess.CalledProcessError as err:
    #         # print('e.output: ', e.output)
    #         xml_out += err.output.decode(enc)

    return str_out, xml_out


def _execute_command2(str_command, timeout=0):

    import ctypes
    from subprocess import check_output
    import subprocess

    enc = 'cp%d' % ctypes.windll.kernel32.GetOEMCP()

    args = [os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + r'\exec\vlc-2.1.6\vlc.bat','']
    # args = [os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + r'\exec\vlc-2.1.6\vlc.exe ','--intf=qt  --extraintf=http --http-password=63933 --quiet --file-logging']
    process_vlc = subprocess.Popen(args, stdout=subprocess.PIPE, shell=False)

    xml_out = ''
    str_out = ''

    return str_out, xml_out


def mosaic_func(action):

    import pyautogui

    configureMosaic_exe = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + r'\exec\Mosaic\configureMosaic-32bit-64bit.exe '

    str_param = ''
    str_out = ''
    str_code = ''
    if action == "Start":
        print("Start mosaic")
        # str_param = 'set cols=1 rows=2 res=1280,720,60 out=0,0 out=0,1'
        str_param = 'set cols=2 rows=4 res=1280,768,60 out=0,0 out=0,1 out=0,2 out=0,3 out=1,0 out=1,1 out=1,2 out=1,3'
        # str_param = 'set rows=1 cols=7 res=1280,768,60 out=0,0 out=0,1 out=0,2 out=0,3 out=1,0 out=1,1 out=1,2'

        pyautogui.keyDown('shift', 'S')

    elif action == "Stop":
        print("Stop mosaic")

        result = None
        for process in (process for process in psutil.process_iter() if process.name() == "chrome.exe"):
            result = process.kill()

        str_out += 'Stoped chrome.exe\n'
        str_out += str(result) + '\n'

        str_param = 'disable'

    elif action == "Restart":
        print("Restart mosaic")
        wt.Show()
        str_param = 'help'

    elif action == "State":
        print("State mosaic")
        str_param = 'query current'

    output_str_xml = _execute_command(configureMosaic_exe + str_param)
    str_out += output_str_xml[0]
    xml_out = output_str_xml[1]

    if action == "Restart":  # Temporary!
        print("mosaic help")
        str_out = xml_out

    else:
        doc_dict = xmltodict.parse(xml_out)  # Parse the read document string
        pprint.pprint(doc_dict)

        if 'error' in doc_dict:
            grid_err = doc_dict['error']['#text']
            str_out += '\n' + grid_err + '\n'
            if grid_err == 'NvAPI_Mosaic_SetDisplayGrids failed: NVAPI_ERROR':
                if action == "Start":
                    str_out += "EnableOneProjector"
                if action == "Stop":
                    str_out += "Уже мозаика разобрана"
            if action == "Start" and grid_err == 'Output index 2 on GPU 0 is out of bounds':
                str_out += "Включите проекторы"
            if action == "Stop" and grid_err == 'No connected outputs found':
                str_out += "Невозможно разобрать мозаику"
        else:
            str_out += xml_out

            if action == "State":

                grids = doc_dict['query']['grids']
                if grids is None:
                    str_out += "Projectors disabled"
                    str_code = "Projectors disabled"
                else:
                    rows = doc_dict['query']['grids']['grid']['@rows']
                    cols = doc_dict['query']['grids']['grid']['@columns']
                    if rows == "1" and cols == "8":
                        str_out += "Mosaic enabled"
                        str_code = "Mosaic enabled"
                    elif rows == "1" and cols == "1":
                        str_out += "Mosaic disabled"
                        str_code = "Mosaic enabled"

    return str_out, str_code


def vlc_func(action):

    vlc_exe = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + r'\exec\vlc-2.1.6\vlc.bat'

    str_out = ''
    if action == "Start":
        print("Start vlc")
        # str_param = '--intf=qt  --extraintf=http:rc --http-password=63933 --quiet --file-logging'
        # str_param = '--intf=qt  --extraintf=http --http-password=63933 --quiet --file-logging'
        # str_param = '--extraintf=http --http-password=63933 --quiet --qt-start-minimized'
        # str_param = '--extraintf=http --http-password=63933 --quiet'
        # без интерфейса https://wiki.videolan.org/VLC_command-line_help/
        # str_param = 'vlc -Ihttp'
        # str_param = 'vlc --intf=http'
        str_param = ''

        output_str_xml = _execute_command2(vlc_exe + str_param)
        str_out += output_str_xml[0]

    if action == "Stop":
        print("Stop vlc")
        # str_param = 'TASKKILL /F /IM vlc.exe'
        # str_param = 'TASKKILL /IM vlc.exe'
        # os.system(str_param)
        result = None
        for process in (process for process in psutil.process_iter() if process.name() == "vlc.exe"):
            result = process.kill()

        str_out = 'Stoped vlc.exe' + str(result)

    return str_out


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


def displaypro_func(action):

    displaypro_exe = r'c:\Program Files (x86)\Immersive Display PRO\ImmersiveDisplayPro.bat '

    str_out = ''
    if action == "Start":
        print("Start displaypro")
        str_param = ''

        output_str_xml = _execute_command1(displaypro_exe + str_param)
        str_out += output_str_xml[0]

    if action == "Stop":
        result = None
        for process in (process for process in psutil.process_iter() if process.name() == "ImmersiveDisplayPro.exe"):
            result = process.kill()

        str_out = 'Stoped ImmersiveDisplayPro.exe' + str(result)

    return str_out


def base_func(action):

    str_out = ''
    if action == "Start":
        print("Start")

        str_out = winapi_func('EnableOneProjector')
        # ToDo Bad mode
        if str_out != "Включите проекторы":
            str_out += '\n' + mosaic_func('Start')[0]
            # ToDo Check mosaic is ok

            str_out += '\n' + displaypro_func('Start')
            # time.sleep(20)

            str_out += '\n' + vlc_func('Start')
        else:
            str_out += '\n' + 'Повторно запустите систему'

    elif action == "Stop":
        print("Stop system")
        str_out += '\n' + vlc_func('Stop')
        str_out += '\n' + displaypro_func('Stop')
        str_out += '\n' + mosaic_func('Stop')[0]
        str_out += '\n' + winapi_func('setPrimaryMonitor')

    else:
        str_out = "Base: Unnoun command"

    return str_out


