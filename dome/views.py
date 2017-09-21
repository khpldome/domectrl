from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import View, TemplateView
import xmltodict
import pprint

# import win32api as w
# import win32con as c


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


def mosaic_func(action):

    import os
    import ctypes
    from subprocess import check_output
    import subprocess

    enc = 'cp%d' % ctypes.windll.kernel32.GetOEMCP()
    configureMosaic_exe = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + r'\exec\Mosaic\configureMosaic-32bit-64bit.exe '

    str_param = ''
    if action == "Start":
        print("Start mosaic")
        str_param = 'set rows=1 cols=8 res=1280,768,60 out=0,0 out=0,1 out=0,2 out=0,3 out=1,0 out=1,1 out=1,2 out=1,3'
        str_param = 'set rows=1 cols=7 res=1280,768,60 out=0,0 out=0,1 out=0,2 out=0,3 out=1,0 out=1,1 out=1,2'

    elif action == "Stop":
        print("Stop mosaic")
        str_param = 'disable'

    elif action == "Restart":
        print("Restart mosaic")
        str_param = 'help'

    elif action == "State":
        print("State mosaic")
        str_param = 'query current'

    out = None
    try:
        # check_output('>&2 echo "errrrr"; exit 1', shell=True)
        out = check_output(configureMosaic_exe + str_param, shell=True)
    except subprocess.CalledProcessError as e:
        print('e.output: ', e.output)
        out = e.output
    # out = check_output(configureMosaic_exe + str_param, shell=True)

    # doc_dict = xmltodict.parse(out)  # Parse the read document string
    # pprint.pprint(doc_dict)
    #
    # print(doc_dict['query']['grids']['grid']['@rows'])
    # print(doc_dict['query']['grids']['grid']['@columns'])
    print(out)

    # print(sys.getdefaultencoding())
    # print(locale.getpreferredencoding())
    # print(sys.stdout.encoding)
    # print(sys.stderr.encoding)

    return out


def vlc_func(action):

    import os
    import ctypes
    from subprocess import check_output

    enc = 'cp%d' % ctypes.windll.kernel32.GetOEMCP()
    vlc_exe = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + r'\exec\vlc-2.1.6\vlc.exe '

    str_param = ''
    if action == "Start":
        print("Start vlc")
        str_param = '--intf=qt  --extraintf=http:rc --http-password=6393363933 --quiet --file-logging'
        # str_param = '--intf=qt  --extraintf=http:rc --http-password=6393363933 --file-logging'

    out = check_output(vlc_exe+str_param, shell=True)
    print(out.decode(enc))

    return out.decode(enc)