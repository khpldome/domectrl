

from django.conf import settings
from django.conf.urls import url, include

from . import views

import filemanager

app_name = "domeplaylist"


playlist_urls = [

    url(r'^add/$', views.PlayItemAddView.as_view(), name='add_item'),
    # url(r'^del/$', views.PlayItemAddView.as_view(), name='delete_item'),

    # url(r'^new-page/(?P<page_type>[0-9a-zA-Z_-]{1,30})/$', views.NewPageFormView.as_view(), name='new_page'),
    url(r'^new-playitem/$', views.NewPlayItemFormView.as_view(), name='new_playitem'),

    url(r'^playitem/(?P<playitem_id>\d+)/edit/$', views.EditPlayItemFormView.as_view(), name='edit_playitem'),
    url(r'^playitem/(?P<playitem_id>\d+)/delete/$', views.DeletePlayItemView.as_view(), name='delete_playitem'),
    url(r'^playitem/(?P<playitem_id>\d+)/play/$', views.PlayItemPlayView.as_view(), name='play_playitem'),

    # url(r'^picker/', include('filemanager.urls', namespace="filemanager")),
    # url(r'^picker/', filemanager.urls),
]


urlpatterns = [



    url(r'^playlist/(?P<playlist_id>\d+)/', include(playlist_urls)),

    url(r'^dashboard/$', views.DashboardView.as_view(), name='dashboard'),

    url(r'^new-playlist/$', views.NewPlayListView.as_view(), name='new_playlist'),

    url(r'^no-access/$', views.NoAccessView.as_view(), name='no_access'),

]
