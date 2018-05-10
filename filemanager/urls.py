from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from filemanager.views import BrowserView, TrackAddView, DetailView,  TrackSelectView
from filemanager.views import UploadView, UploadFileView, DirectoryCreateView #NavigateView


app_name = "filemanager"


urlpatterns = [
    url(r'^(?P<playlist_id_active>-?\d+)/$', BrowserView.as_view(), name='browser'),
    url(r'^detail/$', DetailView.as_view(), name='detail'),
    url(r'^upload/$', UploadView.as_view(), name='upload'),
    url(r'^upload/file/$', csrf_exempt(UploadFileView.as_view()), name='upload-file'),
    url(r'^create/directory/$', DirectoryCreateView.as_view(), name='create-directory'),

    url(r'^track-add/(?P<playlist_id_active>-?\d+)/$', TrackAddView.as_view(), name='track-add'),
    url(r'^track-select/(?P<playlist_id_active>-?\d+)/$', TrackSelectView.as_view(), name='track-select'),
    # url(r'^navigate/(?P<playlist_id_active>-?\d+)/$', NavigateView.as_view(), name='navigate'),
]
