from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import View, TemplateView
import xmltodict
import pprint

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

            text_output = mosaic_func(mosaic_action)

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


def _execute_command(str_command):

    import ctypes
    from subprocess import check_output
    import subprocess

    enc = 'cp%d' % ctypes.windll.kernel32.GetOEMCP()
    try:
        out = check_output(str_command, shell=True, timeout=1)
    except subprocess.CalledProcessError as err:
        # print('e.output: ', e.output)
        out = err.output
    except subprocess.TimeoutExpired as err:
        out = "timeout 1 sec".encode()

    return out.decode(enc)


def mosaic_func(action):

    import os

    configureMosaic_exe = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + r'\exec\Mosaic\configureMosaic-32bit-64bit.exe '

    str_param = ''
    if action == "Start":
        print("Start mosaic")
        str_param = 'set rows=1 cols=8 res=1280,768,60 out=0,0 out=0,1 out=0,2 out=0,3 out=1,0 out=1,1 out=1,2 out=1,3'
        # str_param = 'set rows=1 cols=7 res=1280,768,60 out=0,0 out=0,1 out=0,2 out=0,3 out=1,0 out=1,1 out=1,2'

    elif action == "Stop":
        print("Stop mosaic")
        str_param = 'disable'

    elif action == "Restart":
        print("Restart mosaic")
        str_param = 'help'

    elif action == "State":
        print("State mosaic")
        str_param = 'query current'

    str_res = ''
    str_res = _execute_command(configureMosaic_exe + str_param)

    if action == "Restart":
        print("mosaic help")
    else:
        doc_dict = xmltodict.parse(str_res)  # Parse the read document string
        pprint.pprint(doc_dict)

        if 'error' in doc_dict:
            grid_err = doc_dict['error']['#text']
            if action == "Start" and grid_err == 'NvAPI_Mosaic_SetDisplayGrids failed: NVAPI_ERROR':
                str_res = "NvAPI_Mosaic_SetDisplayGrids failed: NVAPI_ERROR\n 'EnableOneProjector'"
            if action == "Start" and grid_err == 'Output index 2 on GPU 0 is out of bounds':
                str_res = "Output index 2 on GPU 0 is out of bounds\n 'Включите проекторы'"

    return str_res


def vlc_func(action):

    import os
    import psutil

    vlc_exe = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + r'\exec\vlc-2.1.6\vlc.exe '

    str_res = ''
    if action == "Start":
        print("Start vlc")
        str_param = '--intf=qt  --extraintf=http:rc --http-password=6393363933 --quiet --file-logging'
        str_param = '--intf=qt  --extraintf=http --http-password=6393363933 --quiet --file-logging'
        # str_param = '--extraintf=http --http-password=6393363933 --quiet --qt-start-minimized'
        # str_param = '--extraintf=http --http-password=6393363933 --quiet'

        str_res = _execute_command(vlc_exe + str_param)

    if action == "Stop":
        print("Stop vlc")
        # str_param = 'TASKKILL /F /IM vlc.exe'
        # str_param = 'TASKKILL /IM vlc.exe'
        # os.system(str_param)

        for process in (process for process in psutil.process_iter() if process.name() == "vlc.exe"):
            process.kill()

        str_res = 'Stoped vlc.exe'

    return str_res


def winapi_func(action):

    res = None
    out = ''
    if action == "setPrimaryMonitor":
        out = wt.enableLG()
    elif action == "EnableOneProjector":
        res = wt.enableOneProjector()
        # ToDo Bad mode
        if res[1] == -2:
            out = "Включите проекторы"
        else:
            res = wt.enableOneProjector()
    elif action == "WinapiInfo":
        out = wt.winApiInfo()
    else:
        out = "WinAPI: Unnoun command"

    return out, res


def displaypro_func(action):

    import psutil
    displaypro_exe = r'c:\Program Files (x86)\Immersive Display PRO\ImmersiveDisplayPro.bat '

    str_res = ''
    if action == "Start":
        print("Start displaypro")
        str_param = ''
        str_res = _execute_command(displaypro_exe + str_param)

    if action == "Stop":

        for process in (process for process in psutil.process_iter() if process.name() == "ImmersiveDisplayPro.exe"):
            process.kill()

        str_res = 'Stoped ImmersiveDisplayPro.exe'

    return str_res


def base_func(action):

    out_str = ''
    if action == "Start":
        print("Start")

        output = winapi_func('EnableOneProjector')
        out_str = output[0]
        # ToDo Bad mode
        if output[1][1] == 0:
            temp_str = mosaic_func('Start')
            out_str += '\n' + temp_str
            # ToDo Check mosaic is ok

            out_str += '\n' + displaypro_func('Start')
            out_str += '\n' + vlc_func('Start')
        else:
            out_str += '\n' + 'Повторно запустите систему'

    elif action == "Stop":
        print("Stop system")
        out_str += '\n' + mosaic_func('Stop')
        out_str += '\n' + winapi_func('setPrimaryMonitor')[0]
        out_str += '\n' + vlc_func('Stop')
        out_str += '\n' + displaypro_func('Stop')

    else:
        out_str = "Base: Unnoun command"

    return out_str


