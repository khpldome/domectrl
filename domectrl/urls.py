"""domectrl URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf.urls import include, url


urlpatterns = [

    # url(r'^admin/filebrowser/', include(site.urls)),
    # url(r'^grappelli/', include('grappelli.urls')),

    url(r'^admin/', admin.site.urls),

    url(r'^account/', include('domeuser.urls')),

    url(r'^dome/', include('dome.urls')),

    url(r'^', include('domeplaylist.urls')),

    url(r'^picker/', include('filemanager.urls', namespace='filemanager')),

]


