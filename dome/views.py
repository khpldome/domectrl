
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import View, TemplateView

from controlapp import mosaic_surround as mr
from controlapp import vlc_routine as vr
from controlapp import displaypro_routine as dr
from controlapp import winapi_routine as wr
from controlapp import auto_manager as am


def index(request):
    context = {'latest_question_list': 22}
    return render(request, 'dome/index.html', context)


class MosaicActionView(TemplateView):

    template_name = 'dome/index.html'

    def get(self, request, *args, **kwargs):
        # print("get=", mosaic_action)
        messages.error(request, 'mosaic_action=' + kwargs['mosaic_action'])
        return super(MosaicActionView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MosaicActionView, self).get_context_data(**kwargs)
        text_output = ""
        if 'mosaic_action' in kwargs:
            mosaic_action = kwargs['mosaic_action']
            print("mosaic_action=", mosaic_action)

            text_output = mr.mosaic_surround_func(mosaic_action)[0]

        if 'vlc_action' in kwargs:
            vlc_action = kwargs['vlc_action']
            print("vlc_action=", vlc_action)

            text_output = vlc_func(vlc_action)

        context.update({
            "data_context": text_output,
        })
        return context


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

            text_output = vr.vlc_func(vlc_action)

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

            text_output = wr.winapi_func(winapi_action)

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

            text_output = dr.displaypro_func(displaypro_action)

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

            text_output = am.base_func(base_action)

        context['data_context'] = text_output
        return context


