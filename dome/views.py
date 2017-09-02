from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import View, TemplateView
import xmltodict
import pprint


from django.views import View


def index(request):
    context = {'latest_question_list': 22}
    return render(request, 'dome/index.html', context)


class StoreDirectView(TemplateView):

    template_name = 'dome/index.html'

    def get(self, request, *args, **kwargs):
        # print("get=", mosaic_action)

        # messages.error(request, 'User already has this module.')
        # return HttpResponse('Result: ' + text_output)

        return super(StoreDirectView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(StoreDirectView, self).get_context_data(**kwargs)
        if 'mosaic_action' in kwargs:
            mosaic_action = kwargs['mosaic_action']
            print("get=", mosaic_action)

            text_output = ""
            text_output = start_mosaic(mosaic_action)

        # context['pages'] = ModulePage.objects.filter(module_id=self.mymodule.id)
        context.update({
            "data_context": text_output,
            "revenue_shared": 22,
        })
        return context

    # def get_success_url(self):
    #     # Get clone id
    #     return reverse_lazy('monetize_module', kwargs={'module_id': module_id})



def start_mosaic(mode):
    print("Stsrt mosaic")
    import os
    import ctypes
    from subprocess import check_output

    enc = 'cp%d' % ctypes.windll.kernel32.GetOEMCP()
    pathMosaic = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+r'\exec\Mosaic\configureMosaic-32bit-64bit.exe'
    pathVLC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+r'\exec\vlc\vlc.exe'
    # MOSAIC_ENABLE = 'set rows=1 cols=8 res=1280,768,60 out=0,0 out=0,1 out=0,2 out=0,3 out=1,0 out=1,1 out=1,2 out=1,3'
    # MOSAIC_DISABLE = 'disable'

    if mode == "Start":
        str_param = 'set rows=1 cols=8 res=1280,768,60 out=0,0 out=0,1 out=0,2 out=0,3 out=1,0 out=1,1 out=1,2 out=1,3'

    elif mode == "Stop":
        str_param = 'disable'

    elif mode == "Restart":
        str_param = 'help'

    elif mode == "State":
        str_param = 'query current'

    # out = check_output([pathVLC])
    # out = check_output([pathMosaic, str_param])
    out = check_output([pathMosaic, 'query', 'current'])

    doc_dict = xmltodict.parse(out)  # Parse the read document string
    pprint.pprint(doc_dict)

    print(doc_dict['query']['grids']['grid']['@rows'])
    print(doc_dict['query']['grids']['grid']['@columns'])
    print(out.decode(enc))

    # print(sys.getdefaultencoding())
    # print(locale.getpreferredencoding())
    # print(sys.stdout.encoding)
    # print(sys.stderr.encoding)
    # print(pathMosaic)

    return out.decode(enc)
