from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy
from domeuser.models import User, update_member
import logging
from domectrl import settings

logger = logging.getLogger(__name__)


class MadcramAdminSite(AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = ugettext_lazy('Madcram admin')

    # Text to put in each page's <h1>.
    site_header = ugettext_lazy('Madcram administration')

    # Text to put at the top of the admin index page.
    index_title = ugettext_lazy('Madcram site administration')


def push_to_mailchimp(modeladmin, request, queryset):
    merge_field = '*|FNAME|*'
    errors = 0
    pushed = 0
    for user in queryset:
        print(user.email)
        try:
            update_member(user)
            pushed += 1
        except Exception as e:
            logger.error(e)
            errors += 1
            if settings.DEBUG:
                raise
    modeladmin.message_user(request, "%s user emails successfully pushed to MailChimp. %s errors." % (pushed, errors))


push_to_mailchimp.short_description = "Push selected user emails to MailChimp"


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_name',
        'email',
        'date_joined',
        'last_login',
    )
    exclude = ('password',)
    actions = [push_to_mailchimp]


admin.site = MadcramAdminSite()
admin.site.register(User, UserAdmin)
