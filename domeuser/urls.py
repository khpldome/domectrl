from django.conf.urls import url
from django.contrib.auth.views import password_reset_done, password_reset_complete

from domeuser.forms import PassResetRequestForm
from domeuser import views

app_name = "domeuser"

urlpatterns = [
    url(r'^$', views.AccountView.as_view(), name='account'),
    url(r'^sign-in/$', views.SignInView.as_view(), name='sign_in'),
    url(r'^sign-out/$', views.SignOutView.as_view(), name='sign_out'),
    url(r'^registration/$', views.RegistrationView.as_view(), name='registration'),
    url(r'^registration-sign-in/$', views.reg_sign_in, name='reg_sign_in'),
    url(r'^password-reset/request/$', views.password_reset,
        {'password_reset_form': PassResetRequestForm}, name='password_reset'),
    url(r'^password-reset/request/sent/$', password_reset_done, name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[0-9a-zA-Z_\-]+)/(?P<token>[0-9a-zA-Z]{1,13}-[0-9a-zA-Z]{1,20})/$',
        views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^password-reset/complete/$', password_reset_complete, name='password_reset_complete'),
    url(r'^edit/api/$', views.AccountAjaxEdit.as_view()),
]
