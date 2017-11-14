
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from domectrl import settings
# import mailchimp
import logging
from django.db.models.signals import pre_save
from django.dispatch import receiver


logger = logging.getLogger(__name__)


class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')
        if not first_name:
            raise ValueError('User must have a name')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.first_name = first_name
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, password):
        user = self.create_user(email, password=password, first_name=first_name)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    email = models.EmailField("Email Address", max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField("Created", default=timezone.now)
    randomize = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    def __str__(self):
        return "ID: {}. first_name: {}. email: {}".format(self.id, self.first_name, self.email)


    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        return self.first_name

    def get_short_name(self):
        return self.first_name

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        return True


@receiver(pre_save, sender=User)
def user_pre_save(sender, instance, raw, using, update_fields, **kwargs):
    """When user change its email, we want to update our mailing list"""
    try:
        update_member(instance)

    # on production, this app must not block the user
    except Exception as e:
        logger.error(e)
        # if settings.DEBUG:
        #     raise
        # raise
    except:
        pass


def update_member(user):
    """User change info's, we want to update our mailing list

    :param user: Django User model
    """
    # if not settings.MAILCHIMP_API_KEY:
    #     raise ValueError('MAILCHIMP_API_KEY not set!')
    #
    # if not settings.MAILCHIMP_LIST_NAME:
    #     raise ValueError('MAILCHIMP_LIST_NAME not set!')
    #
    # # Has old value ? (on update user)
    # old_user = None
    # if user.pk:
    #     # we retrieve the old user object
    #     old_user = user.__class__.objects.get(pk=user.pk)
    #
    #     # Mailchimp value not changed, we quit.
    #     if not [True for k in settings.MAILCHIMP_ASSOC.values() if getattr(old_user, k) != getattr(user, k)]:
    #         # return
    #         pass
    #
    # # Get user info's
    # infos = {m: getattr(user, u) for m, u in settings.MAILCHIMP_ASSOC.items()}
    #
    # # email required for Mailchimp (user created by django admin has not email)
    # if not infos.get('EMAIL'):
    #     logger.warning('User %s has no email' % user)
    #     return
    #
    # # Get api object and mailing list id
    # api = mailchimp.Mailchimp(settings.MAILCHIMP_API_KEY)
    # # list_id = api.lists.list({'name': settings.MAILCHIMP_LIST_NAME})['data'][0]['id']
    #
    # # send to mailchimp
    # email = {'email': getattr(old_user, 'email', infos['EMAIL'])}
    # try:
    #     # print(">>> email=", email, "infos=", infos,)
    #     result = api.lists.subscribe(settings.MAILCHIMP_LIST_ID, email, infos, double_optin=False, update_existing=True)
    #     # print("<<< result=", result)
    # except:
    #     # raise ValueError('MAILCHIMP subscribe error')
    #     logger.warning('User %s has bad email' % user)

    return
