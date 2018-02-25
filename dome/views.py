
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
from controlapp import projectors_routine as pr


def index(request):
    context = {'latest_question_list': 22}
    return render(request, 'dome/index.html', context)


class MosaicSurroundActionView(TemplateView):

    template_name = 'dome/index.html'

    def get(self, request, *args, **kwargs):
        # print("get=", mosaic_action)
        messages.error(request, 'action=' + kwargs['action'])
        return super(MosaicSurroundActionView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MosaicSurroundActionView, self).get_context_data(**kwargs)
        text_output = ""
        if 'action' in kwargs:
            action = kwargs['action']
            print("action=", action)

            str_context = mr.mosaic_surround_func(action)['verbose']

        context.update({
            "data_context": str_context,
        })
        return context


class VlcActionView(TemplateView):

    template_name = 'dome/index.html'

    def get(self, request, *args, **kwargs):
        return super(VlcActionView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(VlcActionView, self).get_context_data(**kwargs)

        if 'action' in kwargs:
            action = kwargs['action']
            print("action=", action)

            res_dict = vr.vlc_func(action)

        context['data_context'] = res_dict['verbose']
        if 'proc_state' in res_dict:
            context['vlc_state'] = res_dict['proc_state']
        if 'server_state' in res_dict:
            context['vlc_server_state'] = res_dict['server_state']
        return context


class WinapiActionView(TemplateView):

    template_name = 'dome/index.html'

    def get(self, request, *args, **kwargs):
        return super(WinapiActionView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(WinapiActionView, self).get_context_data(**kwargs)
        text_output = ""

        if 'action' in kwargs:
            action = kwargs['action']
            print("action=", action)

            text_output = wr.winapi_func(action)

        context['data_context'] = text_output
        return context


class DisplayproActionView(TemplateView):

    template_name = 'dome/index.html'

    def get(self, request, *args, **kwargs):
        return super(DisplayproActionView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DisplayproActionView, self).get_context_data(**kwargs)

        action = ''
        param = ''
        if 'action' in kwargs:
            action = kwargs['action']
            print("action=", action)

        if 'param' in kwargs:
            param = kwargs['param']
            print("param=", param)

        text_output = dr.displaypro_func(action, param)

        context['data_context'] = text_output
        return context


class ProjectorsActionView(TemplateView):

    template_name = 'dome/index.html'

    def get(self, request, *args, **kwargs):
        return super(ProjectorsActionView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProjectorsActionView, self).get_context_data(**kwargs)

        action = ''
        param = ''
        if 'action' in kwargs:
            action = kwargs['action']
            print("action=", action)

        if 'param' in kwargs:
            param = kwargs['param']
            print("param=", param)

        out_dict = pr.projectors_func(action)

        context['data_context'] = out_dict['verbose']
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


