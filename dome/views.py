from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import View, TemplateView


from django.views import View


def index(request):
    context = {'latest_question_list': 22}
    if request.method == 'GET':
        start_mosaic()
    return render(request, 'dome/index.html', context)


class StoreDirectView(View):

    def get(self, request, mosaic_action):
        print("get=", mosaic_action)

        text_output = ""
        if mosaic_action == "Start":
            messages.error(request, 'User already has tsdfghis module.')
            text_output = start_mosaic()

        elif mosaic_action == "Stop":
            messages.error(request, 'User alreaghfgdy has this module.')
            text_output = start_mosaic()

        elif mosaic_action == "Restart":
            messages.error(request, 'User alrefghfgady has this module.')
            text_output = start_mosaic()

        messages.error(request, 'User already has this module.')
        return HttpResponse('Result: ' + text_output)


def start_mosaic():
    print("Stsrt mosaic")
    import os
    import ctypes
    from subprocess import check_output

    enc = 'cp%d' % ctypes.windll.kernel32.GetOEMCP()
    pathMosaic = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+r'\exec\Mosaic\configureMosaic-32bit-64bit.exe'
    pathVLC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+r'\exec\vlc\vlc.exe'
    MOSAIC_ENABLE = 'set rows=1 cols=8 res=1280,768,60 out=0,0 out=0,1 out=0,2 out=0,3 out=1,0 out=1,1 out=1,2 out=1,3'
    MOSAIC_DISABLE = 'disable'

    # out = check_output(['ping', '8.8.8.8'])
    # out = check_output([pathVLC])
    out = check_output([pathMosaic, 'help'])
    print(out.decode(enc))

    # print(sys.getdefaultencoding())
    # print(locale.getpreferredencoding())
    # print(sys.stdout.encoding)
    # print(sys.stderr.encoding)
    print(pathMosaic)

    return out.decode(enc)
