from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm,\
                                      SetPasswordForm
from django.template import loader

try:
    from google.appengine.api import mail as gae_mail
except ImportError:
    pass


from domeuser.models import User


class SignInForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(SignInForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'form-control', 'required': True})
        self.fields['username'].widget.attrs.update({'tabindex': 1})
        self.fields['password'].widget.attrs.update({'tabindex': 2})


class RegForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=50, label='Re-Type Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'email', 'password')

    def __init__(self, *args, **kwargs):
        super(RegForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput()
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'form-control', 'required': True})

    def clean(self):
        cleaned_data = super(RegForm, self).clean()
        if cleaned_data.get('password') and cleaned_data.get('confirm_password') and\
                cleaned_data['password'] != cleaned_data['confirm_password']:
            self.add_error('confirm_password', "passwords don't match")

    def save(self, *args, **kwargs):
        return User.objects.create_user(**self.cleaned_data)


class PassResetRequestForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PassResetRequestForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = 'Email Address'
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'form-control', 'required': True})

    def clean(self):
        cleaned_data = super(PassResetRequestForm, self).clean()
        if not User.objects.filter(email=cleaned_data['email']).exists():
            self.add_error('email', 'There is no such email address')
        return cleaned_data

    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name=None):
        """
        Sends a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())

        if html_email_template_name is not None:
            body = loader.render_to_string(html_email_template_name, context)
        else:
            body = loader.render_to_string(email_template_name, context)

        gae_mail.send_mail(sender=from_email, to=to_email,
                           subject=subject, body=body)


class PassResetChangeForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(PassResetChangeForm, self).__init__(*args, **kwargs)
        self.fields['new_password2'].label = 'Re-Type New Password'
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'form-control', 'required': True})
