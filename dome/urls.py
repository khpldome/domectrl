
from django.conf.urls import url

from . import views


app_name = "dome"

urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^base/$', views.base_index, name='index_base'),

    url(r'^mosaic/(?P<mosaic_action>\w+)/$', views.MosaicActionView.as_view(), name='mosaic'),
    url(r'^vlc/(?P<vlc_action>\w+)/$', views.VlcActionView.as_view(), name='vlc'),
    url(r'^winapi/(?P<winapi_action>\w+)/$', views.WinapiActionView.as_view(), name='winapi'),
    url(r'^displaypro/(?P<action>\w+)/$', views.DisplayproActionView.as_view(), name='displaypro'),
    url(r'^displaypro/(?P<action>\w+)/(?P<param>\w+)/$', views.DisplayproActionView.as_view(), name='displaypro'),

    url(r'^base/(?P<base_action>\w+)/$', views.BaseView.as_view(), name='base'),

]
