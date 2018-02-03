

from django.conf import settings
from django.conf.urls import url, include

from . import views

import filemanager
from proxy import views as pv


app_name = "domeplaylist"


track_urls = [

    # http://127.0.0.1:8000/domeplaylist/playlist/1/track-list/
    url(r'^track-list/$', views.TrackListView.as_view(), name='track-list'),
    # url(r'^track-list/(?P<path>.*)/$', views.TrackListViewRedirect.as_view(), name='track-list-redirect'),

    # http://127.0.0.1:8000/domeplaylist/playlist/1/track-add/
    # url(r'^track-add/$', views.TrackAddView.as_view(), name='track-add'),

    url(r'^track/(?P<track_id>-?\d+)/delete/$', views.TrackDeleteView.as_view(), name='track-delete'),
    url(r'^track/(?P<track_id>-?\d+)/play/$', views.TrackPlayView.as_view(), name='track-play'),
    url(r'^track/(?P<track_id>-?\d+)/play/(?P<path>.*)/$', views.TrackListViewRedirect.as_view(), name='track-play-proxy'),

]


urlpatterns = [

    url(r'^$', views.IndexView.as_view(), name='index'),

    url(r'^playlist/(?P<playlist_id>-?\d+)/', include(track_urls)),
    url(r'^playlist/(?P<playlist_id>-?\d+)/delete/$', views.PlayListDeleteView.as_view(), name='playlist-delete'),

    # http://127.0.0.1:8000/domeplaylist/new-playlist/
    url(r'^new-playlist/$', views.NewPlayListView.as_view(), name='new-playlist'),

    url(r'^no-access/$', views.NoAccessView.as_view(), name='no_access'),

    # url(r'^proxy/(?P<url>.*)$', HttpProxy.as_view(base_url='http://:63933@127.0.0.1:8080')),
    # url(r'^proxy/(?P<url>.*)/$', pv.proxy_view),

    url(r'^proxy/(?P<path>.*)/$', views.myview, name='proxy'),


]

