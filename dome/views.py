
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import View, TemplateView, RedirectView

from controlapp import mosaic_surround as mr
from controlapp import vlc_routine as vr
from controlapp import displaypro_routine as dr
from controlapp import winapi_routine as wr
from controlapp import auto_manager as am
from controlapp import projectors_routine as pr
from controlapp import fds_routine as fr


class IndexView(TemplateView):

    template_name = "dome/additional.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        str_context = "fdrdsfds"
        if 'text_output' in kwargs:
            str_context = kwargs['text_output']

        context.update({
            "data_context": str_context,
        })
        return context


class MosaicSurroundActionView(TemplateView):

    template_name = 'dome/additional.html'
    str_context = ''

    # def get(self, request, *args, **kwargs):
    #     # print("get=", mosaic_action)
    #     messages.error(request, 'action=' + kwargs['action'])
    #     return super(MosaicSurroundActionView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        action = request.POST.get('action')
        # param = request.POST.get('param')
        print('POST:', action)

        self.str_context = mr.mosaic_surround_func(action)['verbose']

        return super(MosaicSurroundActionView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MosaicSurroundActionView, self).get_context_data(**kwargs)
        str_context = ""
        # if 'action' in kwargs:
        #     action = kwargs['action']
        #     print("action=", action)
        #
        #     str_context = mr.mosaic_surround_func(action)['verbose']

        context.update({
            "data_context": self.str_context,
        })
        return context


class VlcActionView(TemplateView):

    template_name = 'dome/additional.html'
    res_dict = {}

    # def get(self, request, *args, **kwargs):
    #     return super(VlcActionView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        action = request.POST.get('action')
        # param = request.POST.get('param')
        print('POST:', action)

        self.res_dict = vr.vlc_func(action)

        return super(VlcActionView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(VlcActionView, self).get_context_data(**kwargs)

        context['data_context'] = self.res_dict['verbose']
        if 'proc_state' in self.res_dict:
            context['vlc_state'] = self.res_dict['proc_state']
        if 'server_state' in self.res_dict:
            context['vlc_server_state'] = self.res_dict['server_state']
        return context


class WinapiActionView(TemplateView):

    template_name = 'dome/additional.html'
    text_output = ''

    def get(self, request, *args, **kwargs):
        return super(WinapiActionView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        action = request.POST.get('action')
        # param = request.POST.get('param')
        print('POST:', action)

        self.text_output = wr.winapi_func(action)

        return super(WinapiActionView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(WinapiActionView, self).get_context_data(**kwargs)

        context['data_context'] = self.text_output
        return context


# class DisplayproActionView(RedirectView):
#
#     text_output = ''
#
#     def get(self, request, *args, **kwargs):
#
#         action = request.GET.get('action', '')
#         param = request.GET.get('param', '')
#         if 'action' is not '':
#             print("action=", action)
#
#         if 'param' is not '':
#             print("param=", param)
#
#         self.text_output = dr.displaypro_func(action, param)
#
#         return super(DisplayproActionView, self).get(request, *args, **kwargs)
#
#     def get_redirect_url(self, *args, **kwargs):
#         return reverse_lazy('dome:index', kwargs={'text_output': str(self.text_output)+'qwewewerwerw'})


class DisplayproActionView(TemplateView):

    template_name = 'dome/additional.html'
    text_output = ''

    # def get(self, request, *args, **kwargs):
    #
    #     action = ''
    #     param = ''
    #     if 'action' in kwargs:
    #         action = kwargs['action']
    #         print("GET:action=", action)
    #
    #     if 'param' in kwargs:
    #         param = kwargs['param']
    #         print("GET:param=", param)
    #
    #     self.text_output = dr.displaypro_func(action, param)
    #
    #     return super(DisplayproActionView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        action = request.POST.get('action')
        # param = request.POST.get('param')

        print('POST:', action)

        self.text_output = dr.displaypro_func(action)
        # self.text_output = str(request.POST)

        return super(DisplayproActionView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DisplayproActionView, self).get_context_data(**kwargs)

        context['data_context'] = self.text_output
        return context


class ProjectorsActionView(TemplateView):

    template_name = 'dome/additional.html'
    out_dict = {}

    def get(self, request, *args, **kwargs):
        return super(ProjectorsActionView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        action = request.POST.get('action')
        # param = request.POST.get('param')

        print('POST:', action)

        self.out_dict = pr.projectors_func(action)
        # self.text_output = str(request.POST)

        return super(ProjectorsActionView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProjectorsActionView, self).get_context_data(**kwargs)

        context['data_context'] = self.out_dict['verbose']
        return context


class FdsActionView(TemplateView):

    template_name = 'dome/additional.html'
    out_dict = {}

    def get(self, request, *args, **kwargs):
        return super(FdsActionView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        action = request.POST.get('action')
        # param = request.POST.get('param')
        print('POST:', action)

        self.out_dict = fr.fds_func(action)

        return super(FdsActionView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(FdsActionView, self).get_context_data(**kwargs)

        # action = ''
        # if 'action' in kwargs:
        #     action = kwargs['action']
        #     print("action=", action)
        #
        #     out_dict = fr.fds_func(action)

        context['data_context'] = self.out_dict['verbose']
        return context


class BaseView(TemplateView):

    template_name = 'dome/additional.html'
    out_dict = {}

    def get(self, request, *args, **kwargs):
        return super(BaseView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        action = request.POST.get('action')
        # param = request.POST.get('param')
        print('POST:', action)

        self.out_dict = am.base_func(action)

        return super(BaseView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)

        context['data_context'] = self.out_dict['verbose']

        return context


