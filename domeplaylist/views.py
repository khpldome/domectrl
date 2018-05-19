# -*- coding: utf-8 -*-
from __future__ import print_function

from django.contrib.auth.mixins import LoginRequiredMixin
# from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import View, TemplateView, ListView, FormView, CreateView, UpdateView, DeleteView

from domeplaylist.forms import PlayListForm, PlayItemForm, PlayItemInlineFormSet
from domeplaylist.models import PlayList, Track
from domeplaylist.mixins import ModulePermissionMixin, AjaxHandlerMixin

import requests
import json

from django.contrib import messages

import utils.executor as ue
from controlapp import vlc_routine as vr
from controlapp import displaypro_routine as dr
from controlapp import mosaic_surround as ms
from controlapp import projectors_routine as pr
import time

from django.conf import settings
import domectrl.config_fds as conf



class IndexView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('domeplaylist:track-list', kwargs={'playlist_id': -1}))
        else:
            return HttpResponseRedirect(reverse_lazy('domeuser:sign_in'))


class NewPlayListView(LoginRequiredMixin, CreateView):
    template_name = 'domeplaylist/new_playlist.html'
    form_class = PlayListForm

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(NewPlayListView, self).get_form_kwargs()
        # kwargs['request'] = self.request
        return kwargs

    # def get_success_url(self):
    #     # return reverse_lazy('choose_page_type', kwargs={'module_id': self.object.id})
    #     return reverse_lazy('domeplaylist:edit_playlist', kwargs={'playlist_id': self.object.id})
    def get_success_url(self):
        return reverse_lazy('domeplaylist:track-list', kwargs={'playlist_id': self.object.id})

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        form.instance.edit_version = True
        return super(NewPlayListView, self).form_valid(form)


class PlayListDeleteView(LoginRequiredMixin, ModulePermissionMixin, DeleteView):

    model = PlayList
    template_name = 'domeplaylist/no_access.html'

    def get_object(self, **kwargs):
        print('myPlaylist=', self.myPlaylist)
        return self.myPlaylist

    def get_success_url(self):
        return reverse_lazy('domeplaylist:track-list', kwargs={'playlist_id': self.kwargs['playlist_id']})

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()

        self.object.delete()
        return HttpResponseRedirect(success_url)


class TrackListView(LoginRequiredMixin, ListView):

    template_name = 'domeplaylist/track_list.html'
    context_object_name = "tracklist_qs"
    tracklist_qs = None
    playlist_qs = None
    active_playlist = None

    def get(self, request, *args, **kwargs):
        return super(TrackListView, self).get(request, *args, **kwargs)

    def get_queryset(self, **kwargs):
        # ToDo Add check if exists
        playlist_id = self.kwargs['playlist_id']

        self.playlist_qs = PlayList.objects.filter(user=self.request.user).order_by('order')

        if self.playlist_qs:

            if playlist_id == '-1':

                first_playlist = self.playlist_qs.order_by('order').first()
                self.active_playlist = first_playlist.id
                self.tracklist_qs = Track.objects.filter(playlist__user=self.request.user,
                                                            playlist_id=first_playlist).order_by('order')
            else:
                self.active_playlist = playlist_id
                self.tracklist_qs = Track.objects.filter(playlist__user=self.request.user,
                                                             playlist_id=playlist_id).order_by('order')
            return self.tracklist_qs
        else:
            HttpResponse("application/json")

    def get_context_data(self, **kwargs):
        context = super(TrackListView, self).get_context_data(**kwargs)

        context['playlists_qs'] = self.playlist_qs
        if self.playlist_qs:
            context['playlist_id_active'] = str(self.active_playlist)
            context['playlist_count'] = self.playlist_qs.count()
        else:
            context['playlist_id_active'] = str(0)
            context['playlist_count'] = 0
        if self.tracklist_qs:
            # context['track_id_active'] = self.kwargs['track_id']
            context['track_count'] = self.tracklist_qs.count()
        else:
            context['track_id_active'] = 0
            context['track_count'] = 0

        if self.tracklist_qs:
            for obj in context['tracklist_qs']:
                instance = Track.objects.filter(id=obj.id).first()
                # print('instance=', instance)
                short_track_info_dict = ue.get_short_track_info(instance.text)

                if short_track_info_dict:
                    obj.codec_name = short_track_info_dict['codec_name']
                    obj.codec_long_name = short_track_info_dict['codec_long_name']
                    obj.r_frame_rate = short_track_info_dict['r_frame_rate']
                    obj.duration = short_track_info_dict['duration']
                    obj.width = short_track_info_dict['width']
                    obj.height = short_track_info_dict['height']

                    obj.bit_rate = short_track_info_dict['bit_rate']

        return context


class TrackActionView(LoginRequiredMixin, ListView):

    template_name = 'domeplaylist/track_list.html'
    context_object_name = "tracklist_qs"
    tracklist_qs = None
    playlist_qs = None
    active_playlist = None

    def get(self, request, *args, **kwargs):

        playlist_id = self.kwargs['playlist_id']
        track_id = self.kwargs['track_id']

        # http://192.168.10.106:8080/requests/status.xml?command=in_enqueue&input=f:\Video\Saw\Gattaca\Gattaca.avi
        # 127.0.0.1:8080/requests/status.xml?command=in_enqueue&input=C:\Users\Public\Videos\Sample Videos\Wildlife.wmv

        if track_id != "-1":

            vr.vlc_func('start')

            if 'action' in kwargs:
                action = kwargs['action']
                print("+++++action=", action)

            if 'val' in kwargs:
                val = kwargs['val']
                print("+++++val=", val)

            instance = Track.objects.filter(id=track_id).first()

            # t3 = instance.text.replace(' ', '%20')
            path = instance.title
            print('http://' + conf.HOST_IP, ':8080/requests/status.xml?command=in_enqueue&input=', path)

            if action == 'play':
                # r = requests.get('http://'+conf.ALLOWED_IP+':8080/requests/status.xml?command=in_enqueue&input='+t3, auth=('', '63933'))
                r = requests.get('http://' + conf.HOST_IP + ':8080/requests/status.xml?command=in_play&input=' + path, auth=('', '63933'))
                print("responce=", r)

            # elif action == 'stop':
            #     r = requests.get('http://' + conf.HOST_IP + ':8080/requests/status.xml?command=pl_stop', auth=('', '63933'))
            #     print("responce=", r)

            elif action == 'fullscreen':
                r = requests.get('http://' + conf.HOST_IP + ':8080/requests/status.xml?command=fullscreen', auth=('', '63933'))
                print("responce=", r)

            # elif action == 'seek':
            #     r = requests.get('http://' + conf.HOST_IP + ':8080/requests/status.xml?command=seek&val=' + val, auth=('', '63933'))
            #     print("responce=", r)
        else:
            pass

        return super(TrackActionView, self).get(request, *args, **kwargs)

    def get_queryset(self, **kwargs):

        playlist_id = self.kwargs['playlist_id']

        self.playlist_qs = PlayList.objects.filter(user=self.request.user).order_by('order')

        if self.playlist_qs:

            if playlist_id == '-1':

                first_playlist = self.playlist_qs.order_by('order').first()
                self.active_playlist = first_playlist.id
                self.tracklist_qs = Track.objects.filter(playlist__user=self.request.user,
                                                         playlist_id=first_playlist).order_by('order')
            else:
                self.active_playlist = playlist_id
                self.tracklist_qs = Track.objects.filter(playlist__user=self.request.user,
                                                         playlist_id=playlist_id).order_by('order')
            return self.tracklist_qs
        else:
            HttpResponse("application/json")

    def get_context_data(self, **kwargs):
        context = super(TrackActionView, self).get_context_data(**kwargs)

        context['playlists_qs'] = self.playlist_qs
        context['playlist_id_active'] = str(self.active_playlist)
        context['track_id_active'] = self.kwargs['track_id']
        context['playlist_count'] = self.playlist_qs.count()
        context['track_count'] = self.tracklist_qs.count()

        for obj in context['tracklist_qs']:
            instance = Track.objects.filter(id=obj.id).first()
            # print('instance=', instance)
            short_track_info_dict = ue.get_short_track_info(instance.text)

            if short_track_info_dict:
                obj.codec_name = short_track_info_dict['codec_name']
                obj.codec_long_name = short_track_info_dict['codec_long_name']
                obj.r_frame_rate = short_track_info_dict['r_frame_rate']
                obj.duration = short_track_info_dict['duration']
                obj.width = short_track_info_dict['width']
                obj.height = short_track_info_dict['height']

                obj.bit_rate = short_track_info_dict['bit_rate']

        return context

    def get_success_url(self):
        return reverse_lazy('domeplaylist:track-list')


class NoAccessView(TemplateView):
    template_name = 'domeplaylist/no_access.html'


class TrackDeleteView(LoginRequiredMixin, ModulePermissionMixin, DeleteView):
# class DeletePlayItemView(LoginRequiredMixin, DeleteView):

    model = Track
    template_name = 'domeplaylist/track_list.html'

    def get_object(self, **kwargs):
        print('myTrack=', self.myTrack)
        return self.myTrack

    def get_success_url(self):
        return reverse_lazy('domeplaylist:track-list', kwargs={'playlist_id': self.kwargs['playlist_id']})

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        print(self.myTrack)
        self.object = self.get_object()
        success_url = self.get_success_url()

        self.object.delete()
        # messages.add_message(request, messages.INFO, 'fefefwef!')
        messages.success(request, 'Track deleted successfully.')
        return HttpResponseRedirect(success_url)


class TrackActionRedirect(View):

    def get(self, request, **kwargs):

        pass
        path = self.kwargs['path']
        print('&' * 100, str(self.request.GET))

        if 'command' in self.request.GET:
            path += '?command=' + self.request.GET['command']

        if 'val' in self.request.GET:
            path += '&val=' + self.request.GET['val']

        print('+' * 100, path)

        return HttpResponseRedirect(reverse_lazy('domeplaylist:proxy', kwargs={'path': path}))


def proxyView(request, path):

    from proxy import views as pv

    global pm

    # pm.update_request_ts()
    pm.update_vlc_state()
    print('!'*100, path)
    if pm.is_vlc_active() is True:

        vlc_server_url = 'http://' + conf.VLC_WEB_DOMAIN + '/' + path
        print(">>> " + vlc_server_url)

        extra_requests_args = {}
        return pv.proxy_view(request, vlc_server_url, extra_requests_args)
    else:
        return HttpResponse(status=503)


# def proxyView(request, path):
#
#     from proxy import views as pv
#
#     global pm
#
#     # pm.update_request_ts()
#     pm.update_vlc_state()
#     print('!'*100, path)
#     if pm.is_vlc_active() is True:
#
#         vlc_server_url = 'http://' + conf.VLC_WEB_DOMAIN + '/' + path
#         print(">>> " + vlc_server_url)
#
#         extra_requests_args = {}
#         return pv.proxy_view(request, vlc_server_url, extra_requests_args)
#     else:
#         return HttpResponse(status=503)


class AjaxProcessStatus(LoginRequiredMixin, ModulePermissionMixin, AjaxHandlerMixin, View):
    """handles only ajax requests"""

    global pm
    # system_state_dict = {}

    def get(self, request, *args, **kwargs):

        if request.is_ajax():

            # pm.update_request_ts()

            pm.update_vlc_state()

            pm.update_dpro_state()

            pm.update_mosaic_state()

            pm.update_prjectors_state()

            json_string = pm.get_process_monitor_json()

            return HttpResponse(json_string, content_type="application/json")

        else:
            return HttpResponse('Bad request', status=400)


class ProcessMonitor:

    process_monitor_dict = {}

    vlc_ts = 0
    vlc_created_at = 0
    vlc_proc = False
    vlc_server = False

    dpro_ts = 0
    dpro_created_at = 0
    dpro_proc = False
    dpro_desktop = False
    dpro_window = False
    dpro_collision = 0

    mosaic_ts = 0
    mosaic = False

    projectors_ts = 0
    projectors = False

    def __init__(self, ts, info=''):
        self.request_ts = ts
        self.info = info

    @staticmethod
    def say_hi_static():
        pass

    def update_request_ts(self):
        self.request_ts = time.time()

    # ---------------------------------------------
    def get_vlc_state(self):
        self.vlc_ts = time.time()

        res_dict = vr.vlc_func('state')
        if 'created_at' in res_dict:
            self.vlc_created_at = res_dict['created_at']
        self.vlc_proc = res_dict['proc_state']
        self.vlc_server = res_dict['server_state']

    def update_vlc_state(self):
        self.request_ts = time.time()
        dt = self.request_ts - self.vlc_ts
        if dt > 5:
            # print('$' * 80, dt, ' vlc ', time.time())
            self.get_vlc_state()
            return True
        return False

    def is_vlc_active(self):
        if self.vlc_proc and self.vlc_server:
            return True
        else:
            return False

    # ---------------------------------------------
    def get_dpro_state(self):
        self.dpro_ts = time.time()

        res_dict = dr.displaypro_func('state')
        self.dpro_proc = res_dict['proc_state']
        if 'created_at' in res_dict:
            self.dpro_created_at = res_dict['created_at']
        self.dpro_desktop = res_dict['proc_state']
        self.dpro_window = res_dict['proc_state']
        if self.dpro_proc and self.vlc_proc:
            self.dpro_collision = int(self.vlc_created_at - self.dpro_created_at)
        else:
            self.dpro_collision = 0

    def update_dpro_state(self):
        # self.request_ts = time.time()
        dt = self.request_ts - self.dpro_ts
        if dt > 7:
            # print('$' * 80, dt, ' dpro ', time.time())
            self.get_dpro_state()
            return True
        return False

    def is_dpro_active(self):
        if self.dpro_proc:
            return True
        else:
            return False

    # ---------------------------------------------
    def get_mosaic_state(self):
        self.mosaic_ts = time.time()

        res_dict = ms.mosaic_func('state')
        self.mosaic = res_dict['code']

    def update_mosaic_state(self):
        # self.request_ts = time.time()
        dt = self.request_ts - self.mosaic_ts
        if dt > 8:
            # print('$' * 80, dt, ' mosaic ', time.time())
            self.get_mosaic_state()
            return True
        return False

    # def is_mosaic_active(self):
    #     dt = self.request_ts - self.mosaic_ts
    #     if dt > 10:
    #         return False
    #     else:
    #         return True

    # ---------------------------------------------
    def get_prjectors_state(self):
        self.projectors_ts = time.time()

        res_dict = pr.projectors_func('state')
        if res_dict['count_on'] == conf.POJECTORS_NUMS:
            self.projectors = True
        else:
            self.projectors = False

    def update_prjectors_state(self):
        # self.request_ts = time.time()
        dt = self.request_ts - self.projectors_ts
        if dt > 39:
            self.get_prjectors_state()
            return True
        return False

    def is_prjectors_active(self):
        if self.projectors:
            return True
        else:
            return False

    # ---------------------------------------------
    def get_process_monitor_json(self):
        self.process_monitor_dict.update({

            'request_ts': self.request_ts,

            'vlc_ts': self.vlc_ts,
            'vlc_proc': self.vlc_proc,
            'vlc_server': self.vlc_server,

            'dpro_ts': self.dpro_ts,
            'dpro_proc': self.dpro_proc,
            'dpro_desktop': self.dpro_desktop,
            'dpro_window': self.dpro_window,
            'dpro_collision': self.dpro_collision,

            'mosaic_ts': self.mosaic_ts,
            'mosaic': self.mosaic,

            'projectors': self.projectors,
        })
        return json.dumps(self.process_monitor_dict, indent=4)

    def __repr__(self):
        return self.process_monitor_dict

    def __str__(self):
        return str(self.process_monitor_dict)


pm = ProcessMonitor(ts=time.time())


class AjaxOrder(LoginRequiredMixin, ModulePermissionMixin, AjaxHandlerMixin, View):
    """handles only ajax requests"""

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            if 'action' in request.POST and hasattr(self, request.POST['action']):
                handler = getattr(self, request.POST['action'])
                return handler(request)
            else:
                return HttpResponse('Action not provided or incorrect', status=400)
        else:
            return HttpResponse('Bad request', status=400)

    def change_playlist_order(self, request):
        order_dict = json.loads(request.POST['order'])
        print(order_dict)
        playlists = PlayList.objects.filter(
            id__in=order_dict.keys()
        ).only('id', 'order')
        for playlist in playlists:
            if playlist.order != order_dict[str(playlist.id)]:
                playlist.order = order_dict[str(playlist.id)]
                playlist.save()

        return HttpResponse(status=204)

    def change_track_order(self, request):
        order_dict = json.loads(request.POST['order'])
        print(order_dict)
        tracks = Track.objects.filter(
            id__in=order_dict.keys()
        ).only('id', 'order')
        for track in tracks:
            if track.order != order_dict[str(track.id)]:
                track.order = order_dict[str(track.id)]
                track.save()

        return HttpResponse(status=204)
