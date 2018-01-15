

from django.conf import settings
from django.conf.urls import url, include

from . import views

import filemanager


app_name = "domeplaylist"


track_urls = [

    # ToDo track-list track-new track-delete track-play

    # http://127.0.0.1:8000/domeplaylist/playlist/1/tracklist/
    url(r'^tracklist/$', views.TrackListView.as_view(), name='track-list'),


    url(r'^add/$', views.PlayItemAddView.as_view(), name='add_item'),
    # url(r'^del/$', views.PlayItemAddView.as_view(), name='delete_item'),

    url(r'^new-playitem/$', views.NewPlayItemFormView.as_view(), name='new_playitem'),

    url(r'^playitem/(?P<playitem_id>\d+)/edit/$', views.EditPlayItemFormView.as_view(), name='edit_playitem'),
    url(r'^playitem/(?P<playitem_id>\d+)/delete/$', views.DeletePlayItemView.as_view(), name='delete-playitem'),
    url(r'^playitem/(?P<playitem_id>\d+)/play/$', views.PlayItemPlayView.as_view(), name='play_playitem'),

    # url(r'^picker/', include('filemanager.urls', namespace="filemanager")),
    # url(r'^picker/', filemanager.urls),
]


urlpatterns = [

    url(r'^playlist/(?P<playlist_id>\d+)/', include(track_urls)),

    # http://127.0.0.1:8000/domeplaylist/user-playlists/
    url(r'^user-playlists/$', views.UserPlaylistsView.as_view(), name='user-playlists'),

    # http://127.0.0.1:8000/domeplaylist/new-playlist/
    url(r'^new-playlist/$', views.NewPlayListView.as_view(), name='new-playlist'),

    url(r'^no-access/$', views.NoAccessView.as_view(), name='no_access'),

]
