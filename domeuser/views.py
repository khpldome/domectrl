import json

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy, reverse
from django.core.validators import EmailValidator
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import resolve_url
from django.template.response import TemplateResponse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, TemplateView, RedirectView, View

from domeplaylist.mixins import AjaxHandlerMixin
from domeuser.forms import RegForm, SignInForm, PassResetChangeForm, PassResetRequestForm

# from domectrl.settings import ADMIN_EMAIL, APP_EMAIL
APP_EMAIL = ""

email_validator = EmailValidator()


class SignInView(FormView):
    template_name = 'domeuser/sign_in.html'
    form_class = SignInForm
    success_url = reverse_lazy('domeplaylist:track-list', kwargs={'playlist_id': -1})

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('domeplaylist:track-list', kwargs={'playlist_id': -1}))

        else:
            return super(SignInView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(SignInView, self).form_valid(form)


def reg_sign_in(request):
    template_name = 'domeuser/reg_sign_in.html'
    success_url = reverse_lazy('domeplaylist:track-list', kwargs={'playlist_id': -1})

    reg_form = RegForm
    sign_in_form = SignInForm

    if request.method == 'POST':
        form_name = request.POST.get('form_name', None)
        if form_name == 'SignInForm':
            sign_in_form = SignInForm(request=request, data=request.POST)
            if sign_in_form.is_valid():
                user = authenticate(email=sign_in_form.cleaned_data['username'], password=sign_in_form.cleaned_data['password'])
                login(request, user)
                return HttpResponseRedirect(success_url)
        else:
            reg_form = RegForm(request.POST)
            if reg_form.is_valid():
                reg_form.save()
                user = authenticate(email=reg_form.cleaned_data['email'], password=reg_form.cleaned_data['password'])
                login(request, user)
                return HttpResponseRedirect(success_url)

    context = {
        'reg_form': reg_form,
        'sign_in_form': sign_in_form,
    }

    if request.user.is_authenticated:
        return HttpResponseRedirect(success_url)
    else:
        return TemplateResponse(request, template_name, context)


class SignOutView(RedirectView):
    url = reverse_lazy('domeuser:sign_in')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(SignOutView, self).get(request, *args, **kwargs)


class RegistrationView(FormView):
    template_name = 'domeuser/reg.html'
    form_class = RegForm
    success_url = reverse_lazy('domeplaylist:track-list', kwargs={'playlist_id': -1})

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('domeplaylist:track-list', kwargs={'playlist_id': -1}))
        else:
            return super(RegistrationView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        userr = form.save()
        user = authenticate(email=form.cleaned_data['email'],
                            password=form.cleaned_data['password'])
        login(self.request, user)
        return super(RegistrationView, self).form_valid(form)


# default django view with changes that after password have been changed,
# user automatically signed in
@sensitive_post_parameters()
@never_cache
def password_reset_confirm(request, uidb64=None, token=None,
                           template_name='registration/password_reset_confirm.html',
                           token_generator=default_token_generator,
                           set_password_form=PassResetChangeForm,
                           post_reset_redirect=None,
                           extra_context=None):
    """
    View that checks the hash in a password reset link and presents a
    form for entering a new password.
    """
    UserModel = get_user_model()
    assert uidb64 is not None and token is not None  # checked by URLconf

    try:
        # urlsafe_base64_decode() decodes to bytestring on Python 3
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        title = 'Enter new password'
        if request.method == 'POST':
            form = set_password_form(user, request.POST)
            if form.is_valid():
                u = form.save()
                user = authenticate(email=u.email,
                                    password=form.cleaned_data['new_password1'])
                if user and user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse_lazy('domeplaylist:track-list', kwargs={'playlist_id': -1}))
                else:
                    return HttpResponseRedirect(reverse_lazy('domeuser:sign_in'))
        else:
            form = set_password_form(user)
    else:
        validlink = False
        form = None
        title = 'Password reset unsuccessful'
    context = {'form': form, 'title': title, 'validlink': validlink, }

    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)


# default django view with changes to send mail through google.appengine.api
@csrf_protect
def password_reset(request, is_admin_site=False,
                   template_name='registration/password_reset_form.html',
                   email_template_name='registration/password_reset_email.html',
                   subject_template_name='registration/password_reset_subject.txt',
                   password_reset_form=PassResetRequestForm,
                   token_generator=default_token_generator,
                   post_reset_redirect=None,
                   from_email=APP_EMAIL,
                   extra_context=None,
                   html_email_template_name=None,
                   extra_email_context=None):
    if post_reset_redirect is None:
        post_reset_redirect = reverse('domeuser:password_reset_done')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': from_email,
                'email_template_name': email_template_name,
                'subject_template_name': subject_template_name,
                'request': request,
                'html_email_template_name': html_email_template_name,
                'extra_email_context': extra_email_context,
            }
            if is_admin_site:
                warnings.warn(
                    "The is_admin_site argument to "
                    "django.contrib.auth.views.password_reset() is deprecated "
                    "and will be removed in Django 1.10.",
                    RemovedInDjango110Warning, 3
                )
                opts = dict(opts, domain_override=request.get_host())
            form.save(**opts)
            return HttpResponseRedirect(post_reset_redirect)
    else:
        form = password_reset_form()

    context = {'form': form, 'title': 'Password reset'}
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)


class AccountView(LoginRequiredMixin, TemplateView):
    template_name = 'domeuser/account.html'


class AccountAjaxEdit(LoginRequiredMixin, AjaxHandlerMixin, View):
    """handles only ajax requests"""

    def change_first_name(self, request):
        request.user.first_name = request.POST['new_name']
        request.user.save()
        return HttpResponse(json.dumps({'name': request.user.first_name}))

    def change_email(self, request):
        if not request.user.check_password(request.POST['pass']):
            return HttpResponse('Password incorrect', status=400)
        try:
            new_email = request.POST['new_email'].strip()
            email_validator(new_email)
            request.user.email = new_email
            request.user.save()
            return HttpResponse(json.dumps({'email': new_email}))
        except ValidationError:
            return HttpResponse('Enter a valid email address', status=400)

    def change_pass(self, request):
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        if pass1 != pass2:
            return HttpResponse('The passwords do not match', status=400)
        if request.user.check_password(request.POST['pass']):
            request.user.set_password(pass1)
            request.user.save()
            return HttpResponse(status=204)
        else:
            return HttpResponse('Incorrect current password', status=400)
