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

        self.playlist_qs = PlayList.objects.filter(user=self.request.user)

        if playlist_id == '-1':

            first_playlist = self.playlist_qs.order_by('pk').first()
            self.active_playlist = first_playlist.id
            self.tracklist_qs = Track.objects.filter(playlist__user=self.request.user,
                                                     playlist_id=first_playlist).order_by('-pk')
        else:
            self.active_playlist = playlist_id
            self.tracklist_qs = Track.objects.filter(playlist__user=self.request.user,
                                                     playlist_id=playlist_id).order_by('-pk')
        return self.tracklist_qs

    def get_context_data(self, **kwargs):
        context = super(TrackListView, self).get_context_data(**kwargs)

        context['playlists_qs'] = self.playlist_qs
        context['playlist_id_active'] = str(self.active_playlist)
        # context['track_id_active'] = self.kwargs['track_id']
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

        # context.update({
        #     'form': StoreSearchForm(),
        # })

        return context


class TrackPlayView(LoginRequiredMixin, ListView):

    template_name = 'domeplaylist/track_list.html'
    context_object_name = "tracklist_qs"
    tracklist_qs = None
    playlist_qs = None
    active_playlist = None

    def get(self, request, *args, **kwargs):

        import time

        playlist_id = self.kwargs['playlist_id']
        track_id = self.kwargs['track_id']

        # http://192.168.10.106:8080/requests/status.xml?command=in_enqueue&input=f:\Video\Saw\Gattaca\Gattaca.avi
        # 127.0.0.1:8080/requests/status.xml?command=in_enqueue&input=C:\Users\Public\Videos\Sample Videos\Wildlife.wmv

        if track_id != "-1":

            vr.vlc_func('Start')

            time.sleep(5)

            instance = Track.objects.filter(id=track_id).first()

            # t3 = instance.text.replace(' ', '%20')
            path = instance.title
            print('http://' + conf.HOST_IP, ':8080/requests/status.xml?command=in_enqueue&input=', path)
            # r = requests.get('http://'+conf.ALLOWED_IP+':8080/requests/status.xml?command=in_enqueue&input='+t3, auth=('', '63933'))
            r = requests.get('http://' + conf.HOST_IP + ':8080/requests/status.xml?command=in_play&input=' + path, auth=('', '63933'))
            print("responce=", r)
        else:
            pass

        return super(TrackPlayView, self).get(request, *args, **kwargs)

    def get_queryset(self, **kwargs):
        # ToDo Add check if exists
        playlist_id = self.kwargs['playlist_id']

        self.playlist_qs = PlayList.objects.filter(user=self.request.user)

        if playlist_id == '-1':

            first_playlist = self.playlist_qs.order_by('pk').first()
            self.active_playlist = first_playlist.id
            self.tracklist_qs = Track.objects.filter(playlist__user=self.request.user,
                                                     playlist_id=first_playlist).order_by('-pk')
        else:
            self.active_playlist = playlist_id
            self.tracklist_qs = Track.objects.filter(playlist__user=self.request.user,
                                                     playlist_id=playlist_id).order_by('-pk')
        return self.tracklist_qs

    def get_context_data(self, **kwargs):
        context = super(TrackPlayView, self).get_context_data(**kwargs)

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


class NoAccessView(TemplateView):
    template_name = 'domeplaylist/no_access.html'


class TrackDeleteView(LoginRequiredMixin, ModulePermissionMixin, DeleteView):
# class DeletePlayItemView(LoginRequiredMixin, DeleteView):

    model = Track
    template_name = 'domeplaylist/no_access.html'

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


class TrackListViewRedirect(View):

    def get(self, request, **kwargs):
        pass

        return HttpResponseRedirect(reverse_lazy('domeplaylist:proxy', kwargs={'path': self.kwargs['path']}))


def proxyView(request, path):

    from proxy import views as pv

    res_dict = vr.vlc_func('state')
    print('path=', path, res_dict['verbose'])

    if res_dict['code'] == 0:
        extra_requests_args = {}
        remoteurl = 'http://' + conf.VLC_WEB_DOMAIN + '/' + path
        return pv.proxy_view(request, remoteurl, extra_requests_args)
    else:
        return HttpResponse(status=503)


class AjaxProcessStatus(LoginRequiredMixin, ModulePermissionMixin, AjaxHandlerMixin, View):
    """handles only ajax requests"""

    system_state_dict = {}

    def get(self, request, *args, **kwargs):

        if request.is_ajax():

            ts = time.time()

            self.system_state_dict.update({
                'request_ts': ts,
                'mosaic_ts': False,
                'mosaic': False,
                'pojectors_ts': False,
                'pojectors': None,
            })

            if 'vlc_ts' in self.system_state_dict:
                dt = self.system_state_dict['request_ts'] - self.system_state_dict['vlc_ts']
                if dt > 20:
                    self.get_vlc_state()
            else:
                self.get_vlc_state()

            if 'dpro_ts' in self.system_state_dict:
                dt = self.system_state_dict['request_ts'] - self.system_state_dict['dpro_ts']
                if dt > 17:
                    self.get_dpro_state()
            else:
                self.get_dpro_state()

            json_string = json.dumps(self.system_state_dict, indent=4)

            return HttpResponse(json_string, content_type="application/json")

        else:
            return HttpResponse('Bad request', status=400)

    def get_vlc_state(self):

        ts = time.time()
        res_dict = vr.vlc_func('state')
        self.system_state_dict.update({
            'vlc_ts': ts,
            'vlc_proccess': res_dict['proc_state'],
            'vlc_server': res_dict['server_state'],
        })
        return True

    def get_dpro_state(self):

        res_dict = dr.displaypro_func('state')
        self.system_state_dict.update({
            'dpro_ts': time.time(),
            'dpro_process': res_dict['proc_state'],
            'dpro_desktop': res_dict['proc_state'],
            'dpro_window': res_dict['proc_state'],
        })
        return True

