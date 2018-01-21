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


class TrackAddView(LoginRequiredMixin, ModulePermissionMixin, UpdateView):

    template_name = 'domeplaylist/edit_playlist.html'
    queryset = PlayList.objects

    form_class = PlayListForm

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(TrackAddView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_object(self, **kwargs):
        return self.myPlaylist

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        path = reverse_lazy('domeplaylist:edit_playlist', kwargs={'playlist_id': self.object.id})
        if self.request.path != path:
            return HttpResponseRedirect(path)
        else:
            return super(TrackAddView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.myPlaylist
        # TODO : check if we edit latest version
        # if not raise Exception()

        return super(TrackAddView, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TrackAddView, self).get_context_data(**kwargs)
        context['pages'] = Track.objects.filter(playlist_id=self.myPlaylist.id)
        return context

    def get_success_url(self):
        playlist_id = self.myPlaylist.id
        return reverse_lazy('domeplaylist:edit_playlist', kwargs={'playlist_id': playlist_id})


class TrackListView(LoginRequiredMixin, ListView):
    template_name = 'domeplaylist/track_list.html'
    context_object_name = "tracklist_qs"
    tracklist_qs = None
    playlist_qs = None
    # playlist_current = None
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
        context['playlist_count'] = self.playlist_qs.count()
        context['track_count'] = self.tracklist_qs.count()

        return context


class TrackPlayView(LoginRequiredMixin, ListView):

    template_name = 'domeplaylist/dashboard.html'
    context_object_name = "playlists"

    def get(self, request, *args, **kwargs):

        playlist_id = self.kwargs['playlist_id']
        track_id = self.kwargs['track_id']

        # http://192.168.10.106:8080/requests/status.xml?command=in_enqueue&input=f:\Video\Saw\Gattaca\Gattaca.avi
        # 127.0.0.1:8080/requests/status.xml?command=in_enqueue&input=C:\Users\Public\Videos\Sample Videos\Wildlife.wmv

        instance = Track.objects.filter(id=track_id)

        t3 = instance.text.replace(' ', '%20')
        print('http://'+conf.ALLOWED_IP, ':8080/requests/status.xml?command=in_enqueue&input=', t3)
        # r = requests.get('http://'+conf.ALLOWED_IP+':8080/requests/status.xml?command=in_enqueue&input='+t3, auth=('', '63933'))
        r = requests.get('http://'+conf.ALLOWED_IP+':8080/requests/status.xml?command=in_play&input='+t3, auth=('', '63933'))
        print(r)

        return super(TrackPlayView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        # res_qs = PlayList.objects.all()
        res_qs = PlayList.objects.filter(user=self.request.user,).order_by('-pk')
        return res_qs

    def get_context_data(self, **kwargs):
        context = super(TrackPlayView, self).get_context_data(**kwargs)

        playitem_qs = Track.objects.all()
        context['playitem_qs'] = playitem_qs
        # context['playitem_qs'] = PlayItem.objects.filter(playlist_id=self.playlist.id)
        # playlist_first = PlayList.objects.filter(user=self.request.user,).order_by('-pk').first()
        # context['playitem_qs'] = PlayItem.objects.filter(playlist_id=playlist_first)
        context['playlist_count'] = PlayList.objects.all().count()
        context['playitem_count'] = Track.objects.all().count()

        return context


    def get_success_url(self):
        return reverse_lazy('dashboard')


class NoAccessView(TemplateView):
    template_name = 'domeplaylist/no_access.html'


# class GenericInfoPageFormView(LoginRequiredMixin, ModulePermissionMixin, FormMixin):
class GenericInfoPageFormView(LoginRequiredMixin, FormMixin):
    """generic form view for all pages, it doesn't handle answers"""

    # template_name = 'madquiz/edit_page.html'
    template_name = 'domeplaylist/edit_playitem.html'
    # form_class = PageEditForm
    form_class = PlayItemForm

    def dispatch(self, request, *args, **kwargs):
        # if 'page_type' in kwargs:
        #     self.page_type = PT_SLUG_DICT[kwargs['page_type']]
        return super(GenericInfoPageFormView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GenericInfoPageFormView, self).get_context_data(**kwargs)
        # if hasattr(self, 'mypage'):
        #     # context['ptitle'] = self.page_type.label
        #     context['back_url'] = reverse_lazy(
        #         'edit_module', kwargs={'module_id': self.kwargs['module_id']}
        #     )
        # elif 'page_type' in self.kwargs:
        #     context['ptitle'] = ''.join(('New ', self.page_type.label))
        #     context['back_url'] = reverse_lazy(
        #         'choose_page_type', kwargs={'module_id': self.kwargs['module_id']}
        #     )
        # context['title'] = self.page_type.label
        # context['page_type'] = self.page_type
        # context['module_id'] = self.mymodule.id
        # if not re.search(r'Page(\s|$)', context['ptitle']):
        #     context['ptitle'] += ' Page'
        return context

    def get_success_url(self):
        # Remove from publish after editing
        # self.mymodule.published_at = None
        # self.mymodule.save(force_update=True)

        # if self.mymodule.cloned_id > 1:
        #     module_id = self.mymodule.cloned_id
        # else:
        #     module_id = self.mymodule.id
        # return reverse_lazy('edit_module', kwargs={'module_id': module_id})

        return reverse_lazy('edit_module', kwargs={'module_id': self.kwargs['module_id']})

    def get_object(self, queryset=None):
        if hasattr(self, 'mypage'):
            return self.mypage
        else:
            return super(GenericInfoPageFormView, self).get_object(queryset)

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = self.initial.copy()
        initial.update({'user_randomize': self.request.user.randomize})
        return initial


class GenericPageFormView(GenericInfoPageFormView):
    """generic form view for all pages with answers handling"""

    def get_answer_formset(self, empty=False):
        # extra = 1 if empty or (
        #     self.page_type.answer == 'text' and not
        #     hasattr(self, 'mypage')
        # ) or (
        #     self.page_type.answer == 'text' and
        #     hasattr(self, 'mypage') and
        #     self.mypage.answer_set.all().count() == 0
        #     ) else 0

        # can_delete = True if hasattr(self, 'mypage') and not empty else False
        # form = TextAnswerForm if self.page_type.answer == 'text' else AnswerForm
        # answer_form_set = inlineformset_factory(
        #     ModulePage, Answer, form,
        #     formset=AnswerInlineFormSet,
        #     extra=extra,
        #     can_delete=can_delete,
        #     # can_order=True,
        # )
        form = PlayItemForm

        '''
        def inlineformset_factory(parent_model, model, form=ModelForm,
                                  formset=BaseInlineFormSet, fk_name=None,
                                  fields=None, exclude=None, extra=3, can_order=False,
                                  can_delete=True, max_num=None, formfield_callback=None,
        '''
        answer_form_set = inlineformset_factory(
            PlayList, Track, form,
            formset=PlayItemInlineFormSet,
            extra=True,
            can_delete=True,
            can_order=True,
             )
        formset_kwargs = {'prefix': 'answer'}
        if not empty:
            if self.request.method == 'POST':
                formset_kwargs.update({'data': self.request.POST})
            # if hasattr(self, 'mypage'):
            #     formset_kwargs.update({'instance': self.mypage})
        return answer_form_set(**formset_kwargs)

    def get_context_data(self, **kwargs):
        if 'answer_formset' not in kwargs:
            answer_formset = self.get_answer_formset()
            kwargs.update({'answer_formset': answer_formset})
        # empty formset is just used for answer form template
        kwargs.update(
            {'empty_answer_formset': self.get_answer_formset(empty=True)}
        )
        return super(GenericPageFormView, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        answer_formset = self.get_answer_formset()
        if form.is_valid() and answer_formset.is_valid():
            # request.user.randomize = form.cleaned_data['randomize']
            request.user.save()
            return self.form_valid(form, answer_formset)
        else:
            return self.form_invalid(form, answer_formset)

    def form_valid(self, form, answer_formset):
        page = form.save()
        answer_formset.instance = page
        answer_formset.save()
        form.instance.updated = True

        # Move module from publish after editing
        # module = page.module
        # module.published_at = None
        # module.save(force_update=True)
        # module.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, answer_formset):
        self.object = None
        return self.render_to_response(
            self.get_context_data(form=form, answer_formset=answer_formset)
        )


class NewPlayItemFormView(GenericPageFormView, CreateView):
    def form_valid(self, form, answer_formset):
        # form.instance.page_type = self.page_type.val
        # form.instance.module_id = self.mymodule.id
        # form.instance.updated = True
        return super(NewPlayItemFormView, self).form_valid(form, answer_formset)


class EditPlayItemFormView(GenericPageFormView, UpdateView):
    def post(self, request, *args, **kwargs):
        self.object = self.mypage
        return super(EditPlayItemFormView, self).post(request, *args, **kwargs)


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
        return HttpResponseRedirect(success_url)
