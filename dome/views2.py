# -*- coding: utf-8 -*-

from __future__ import print_function
import datetime
import json
import re

from django.contrib.auth.mixins import LoginRequiredMixin
# from django.core.mail import send_mail
from django.core.urlresolvers import reverse_lazy, reverse
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import View, TemplateView, ListView, FormView, CreateView, UpdateView, DeleteView
from random import shuffle

from django.views.generic.edit import FormMixin

try:
    from google.appengine.api import mail
except ImportError:
    pass

# from madquiz.forms import StudyModuleForm, ChoosePageTypeForm, PageEditForm, AnswerForm, AnswerInlineFormSet, TextAnswerForm, VideoPageEditForm, MonetizeForm
# from madquiz.models import StudyModule, PT_SLUG_DICT, PT_VAL_DICT, ModulePage, Answer, ShareToken, Payout, UserModule
# from madquiz.mixins import ModulePermissionMixin, AjaxHandlerMixin
# from madcram.settings import ADMIN_EMAIL, APP_EMAIL
from django.core.mail import EmailMessage
from django.contrib import messages

from django.conf import settings


class IndexView(View):
    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse_lazy('dashboard'))
        else:
            return HttpResponseRedirect(reverse_lazy('sign_in'))


class DashboardView(LoginRequiredMixin, ListView):
    # template_name = 'dome/dashboard.html'
    template_name = 'dome/index.html'

    def get(self, request, *args, **kwargs):
        # RecipientView.handle_tokens(request)
        return super(DashboardView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        res_qs = [] #StudyModule.get_dashboard_user_draft_modules(self.request.user)
        return res_qs

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        # published_qs = StudyModule.get_dashboard_user_published_modules(self.request.user)
        # purchased_qs = StudyModule.get_dashboard_user_purchased_modules(self.request.user)
        # shared_qs = StudyModule.get_dashboard_shared_modules_for_user(self.request.user)

        context.update({
            "published_qs": "sdfds",
            "purchased_qs": "sdfs",
            "shared_qs": "sdf",
        })
        return context

