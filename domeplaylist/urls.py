

from django.conf import settings
from django.conf.urls import url, include

from . import views

import filemanager


app_name = "domeplaylist"


track_urls = [

    # http://127.0.0.1:8000/domeplaylist/playlist/1/tracklist/
    url(r'^track-list/$', views.TrackListView.as_view(), name='track-list'),

    # http://127.0.0.1:8000/domeplaylist/playlist/1/track-add/
    url(r'^track-add/$', views.TrackAddView.as_view(), name='track-add'),

    url(r'^track/(?P<track_id>\d+)/delete/$', views.TrackDeleteView.as_view(), name='track-delete'),
    url(r'^track/(?P<track_id>\d+)/play/$', views.TrackPlayView.as_view(), name='track-play'),

]


urlpatterns = [

    url(r'^playlist/(?P<playlist_id>-?\d+)/', include(track_urls)),

    # http://127.0.0.1:8000/domeplaylist/new-playlist/
    url(r'^new-playlist/$', views.NewPlayListView.as_view(), name='new-playlist'),

    url(r'^no-access/$', views.NoAccessView.as_view(), name='no_access'),

]
