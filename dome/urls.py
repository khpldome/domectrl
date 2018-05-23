
from django.conf.urls import url

from . import views


app_name = "dome"

urlpatterns = [

    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<text_output>\w+)/$', views.IndexView.as_view(), name='index'),

    url(r'^mosaic-surround/(?P<action>\w+)/$', views.MosaicSurroundActionView.as_view(), name='mosaic-surround'),
    url(r'^mosaic-surround$', views.MosaicSurroundActionView.as_view(), name='mosaic-surround'),

    url(r'^vlc/(?P<action>\w+)/$', views.VlcActionView.as_view(), name='vlc'),
    url(r'^vlc$', views.VlcActionView.as_view(), name='vlc'),

    url(r'^winapi/(?P<action>\w+)/$', views.WinapiActionView.as_view(), name='winapi'),
    url(r'^winapi$', views.WinapiActionView.as_view(), name='winapi'),

    url(r'^displaypro/(?P<action>\w+)/(?P<param>\w+)/$', views.DisplayproActionView.as_view(), name='displaypro'),
    url(r'^displaypro$', views.DisplayproActionView.as_view(), name='displaypro'),


    url(r'^projectors/(?P<action>\w+)/$', views.ProjectorsActionView.as_view(), name='projectors'),
    url(r'^projectors$', views.ProjectorsActionView.as_view(), name='projectors'),

    url(r'^fds/(?P<action>\w+)/$', views.FdsActionView.as_view(), name='fds'),
    url(r'^fds$', views.FdsActionView.as_view(), name='fds'),

    url(r'^system/(?P<action>\w+)/$', views.BaseView.as_view(), name='system'),
    url(r'^system$', views.BaseView.as_view(), name='system'),

]
