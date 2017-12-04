

from django.conf import settings
from django.conf.urls import url, include

from . import views



playlist_urls = [

    url(r'^edit/$', views.PlayListEditView.as_view(), name='edit_playlist'),

    # url(r'^new-page/(?P<page_type>[0-9a-zA-Z_-]{1,30})/$', views.NewPageFormView.as_view(), name='new_page'),
    url(r'^new-playitem/$', views.NewPageFormView.as_view(), name='new_playitem'),

]


urlpatterns = [

    url(r'^playlist/(?P<playlist_id>\d+)/', include(playlist_urls)),


    url(r'^no-access/$', views.NoAccessView.as_view(), name='no_access'),

]