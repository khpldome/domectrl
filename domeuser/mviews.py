import json
㰤=super
𦺟=None
𘩦=TypeError
ۂ=ValueError
ࠆ=OverflowError
䞚=True
𞢢=False
ﷹ=dict
𗓤=json.dumps
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse_lazy,reverse
from django.core.validators import EmailValidator
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.template.response import TemplateResponse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView,TemplateView,RedirectView,View
from domeuser.forms import RegForm,SignInForm,PassResetChangeForm,PassResetRequestForm
from domeplaylist.mixins import AjaxHandlerMixin
𐦎=""
𐠪=EmailValidator()
class 깘(FormView):
 𐲭='domeuser/sign_in.html'
 ޚ=SignInForm
 ﯠ=reverse_lazy('dashboard')
 def 𫕞(self,𞠿,*args,**kwargs):
  if 𞠿.user.is_authenticated():
   return HttpResponseRedirect(reverse_lazy('dashboard'))
  else:
   return 㰤(깘,self).get(𞠿,*args,**kwargs)
 def 퀜(self,詺):
  쀶(self.request,詺.get_user())
  return 㰤(깘,self).form_valid(詺)
def ﲗ(𞠿):
 𐲭='domeuser/reg_sign_in.html'
 ﯠ=reverse_lazy('dashboard')
 倽=RegForm
 鵨=SignInForm
 if 𞠿.method=='POST':
  䊜=𞠿.POST.get('form_name',𦺟)
  if 䊜=='SignInForm':
   鵨=SignInForm(request=𞠿,data=𞠿.POST)
   if 鵨.is_valid():
    𞤱=authenticate(email=鵨.cleaned_data['username'],password=鵨.cleaned_data['password'])
    쀶(𞠿,𞤱)
    return HttpResponseRedirect(ﯠ)
  else:
   倽=RegForm(𞠿.POST)
   if 倽.is_valid():
    倽.save()
    𞤱=authenticate(email=倽.cleaned_data['email'],password=倽.cleaned_data['password'])
    쀶(𞠿,𞤱)
    return HttpResponseRedirect(ﯠ)
 枳={'reg_form':倽,'sign_in_form':鵨,}
 if 𞠿.user.is_authenticated():
  return HttpResponseRedirect(ﯠ)
 else:
  return TemplateResponse(𞠿,𐲭,枳)
class 𞸤(RedirectView):
 𐨞=reverse_lazy('sign_in')
 def 𫕞(self,𞠿,*args,**kwargs):
  ܓ(𞠿)
  return 㰤(𞸤,self).get(𞠿,*args,**kwargs)
class ق(FormView):
 𐲭='domeuser/reg.html'
 ޚ=RegForm
 ﯠ=reverse_lazy('dashboard')
 def 𫕞(self,𞠿,*args,**kwargs):
  if 𞠿.user.is_authenticated():
   return HttpResponseRedirect(reverse_lazy('dashboard'))
  else:
   return 㰤(ق,self).get(𞠿,*args,**kwargs)
 def 퀜(self,詺):
  𥴶=詺.save()
  𞤱=authenticate(email=詺.cleaned_data['email'],password=詺.cleaned_data['password'])
  쀶(self.request,𞤱)
  return 㰤(ق,self).form_valid(詺)
@sensitive_post_parameters()
@never_cache
def 㷛(𞠿,uidb64=𦺟,token=𦺟,template_name='registration/password_reset_confirm.html',token_generator=default_token_generator,set_password_form=PassResetChangeForm,post_reset_redirect=𦺟,extra_context=𦺟):
 𞡶=get_user_model()
 assert uidb64 is not 𦺟 and token is not 𦺟 
 try:
  飑=force_text(urlsafe_base64_decode(uidb64))
  𞤱=𞡶._default_manager.get(pk=飑)
 except(𘩦,ۂ,ࠆ,𞡶.DoesNotExist):
  𞤱=𦺟
 if 𞤱 is not 𦺟 and token_generator.check_token(𞤱,token):
  𞠨=䞚
  𦣼='Enter new password'
  if 𞠿.method=='POST':
   詺=set_password_form(𞤱,𞠿.POST)
   if 詺.is_valid():
    𡡶=詺.save()
    𞤱=authenticate(email=𡡶.email,password=詺.cleaned_data['new_password1'])
    if 𞤱 and 𞤱.is_active:
     쀶(𞠿,𞤱)
     return HttpResponseRedirect(reverse_lazy('dashboard'))
    else:
     return HttpResponseRedirect(reverse_lazy('sign_in'))
  else:
   詺=set_password_form(𞤱)
 else:
  𞠨=𞢢
  詺=𦺟
  𦣼='Password reset unsuccessful'
 枳={'form':詺,'title':𦣼,'validlink':𞠨,}
 if extra_context is not 𦺟:
  枳.update(extra_context)
 return TemplateResponse(𞠿,template_name,枳)
@csrf_protect
def 쎍(𞠿,is_admin_site=𞢢,template_name='registration/password_reset_form.html',email_template_name='registration/password_reset_email.html',subject_template_name='registration/password_reset_subject.txt',password_reset_form=PassResetRequestForm,token_generator=default_token_generator,post_reset_redirect=𦺟,from_email=𐦎,extra_context=𦺟,html_email_template_name=𦺟,extra_email_context=𦺟):
 if post_reset_redirect is 𦺟:
  post_reset_redirect=reverse('password_reset_done')
 else:
  post_reset_redirect=resolve_url(post_reset_redirect)
 if 𞠿.method=="POST":
  詺=password_reset_form(𞠿.POST)
  if 詺.is_valid():
   𐤆={'use_https':𞠿.is_secure(),'token_generator':token_generator,'from_email':from_email,'email_template_name':email_template_name,'subject_template_name':subject_template_name,'request':𞠿,'html_email_template_name':html_email_template_name,'extra_email_context':extra_email_context,}
   if is_admin_site:
    𘣤.warn("The is_admin_site argument to " "django.contrib.auth.views.password_reset() is deprecated " "and will be removed in Django 1.10.",RemovedInDjango110Warning,3)
    𐤆=ﷹ(𐤆,domain_override=𞠿.get_host())
   詺.save(**𐤆)
   return HttpResponseRedirect(post_reset_redirect)
 else:
  詺=password_reset_form()
 枳={'form':詺,'title':'Password reset'}
 if extra_context is not 𦺟:
  枳.update(extra_context)
 return TemplateResponse(𞠿,template_name,枳)
class 𝜊(LoginRequiredMixin,TemplateView):
 𐲭='domeuser/account.html'
class 𖢠(LoginRequiredMixin,AjaxHandlerMixin,View):
 def 䒻(self,𞠿):
  𞠿.user.first_name=𞠿.POST['new_name']
  𞠿.user.save()
  return 𞢎(𗓤({'name':𞠿.user.first_name}))
 def 𝝜(self,𞠿):
  if not 𞠿.user.check_password(𞠿.POST['pass']):
   return 𞢎('Password incorrect',status=400)
  try:
   જ=𞠿.POST['new_email'].strip()
   𐠪(જ)
   𞠿.user.email=જ
   𞠿.user.save()
   return 𞢎(𗓤({'email':જ}))
  except ValidationError:
   return 𞢎('Enter a valid email address',status=400)
 def 䞉(self,𞠿):
  ﷷ=𞠿.POST['pass1']
  𐤋=𞠿.POST['pass2']
  if ﷷ!=𐤋:
   return 𞢎('The passwords do not match',status=400)
  if 𞠿.user.check_password(𞠿.POST['pass']):
   𞠿.user.set_password(ﷷ)
   𞠿.user.save()
   return 𞢎(status=204)
  else:
   return 𞢎('Incorrect current password',status=400)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
