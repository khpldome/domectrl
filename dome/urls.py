
from django.conf.urls import url

from . import views


app_name = "dome"

urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^base/$', views.base_index, name='index_base'),

    url(r'^mosaic-surround/(?P<action>\w+)/$', views.MosaicSurroundActionView.as_view(), name='mosaic-surround'),
    url(r'^vlc/(?P<action>\w+)/$', views.VlcActionView.as_view(), name='vlc'),
    url(r'^winapi/(?P<action>\w+)/$', views.WinapiActionView.as_view(), name='winapi'),
    url(r'^displaypro/(?P<action>\w+)/$', views.DisplayproActionView.as_view(), name='displaypro'),
    url(r'^displaypro/(?P<action>\w+)/(?P<param>\w+)/$', views.DisplayproActionView.as_view(), name='displaypro'),
    url(r'^projectors/(?P<action>\w+)/$', views.ProjectorsActionView.as_view(), name='projectors'),

    url(r'^base/(?P<base_action>\w+)/$', views.BaseView.as_view(), name='base'),

]
