# -*- coding: utf-8 -*-
from __future__ import print_function

from django.contrib.auth.mixins import LoginRequiredMixin
# from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import View, TemplateView, ListView, FormView, CreateView, UpdateView, DeleteView

from django.views.generic.edit import FormMixin

# try:
#     from google.appengine.api import mail
# except ImportError:
#     pass

from domeplaylist.forms import PlayListForm, PlayItemForm, PlayItemInlineFormSet
from domeplaylist.models import PlayList, Track
from domeplaylist.mixins import ModulePermissionMixin, AjaxHandlerMixin
# from madcram.settings import ADMIN_EMAIL, APP_EMAIL

from django.conf import settings
import domectrl.config_fds as conf

import requests

from django.contrib import messages

import utils.executor as ue


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


def myview(request):
    from proxy import views as pv

    extra_requests_args = {}
    remoteurl = 'http://:63933@127.0.0.1:8080/requests/status.xml'
    return pv.proxy_view(request, remoteurl, extra_requests_args)


class TrackPlayView(LoginRequiredMixin, ListView):

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
            instance = Track.objects.filter(id=track_id).first()

            # t3 = instance.text.replace(' ', '%20')
            path = instance.title
            print('http://' + conf.ALLOWED_IP, ':8080/requests/status.xml?command=in_enqueue&input=', path)
            # r = requests.get('http://'+conf.ALLOWED_IP+':8080/requests/status.xml?command=in_enqueue&input='+t3, auth=('', '63933'))
            r = requests.get('http://' + conf.ALLOWED_IP+ ':8080/requests/status.xml?command=in_play&input=' + path, auth=('', '63933'))
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
