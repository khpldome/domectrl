from __future__ import print_function
from __future__ import print_function
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse

from domeplaylist.models import PlayList, PlayItem

# class ModulePermissionMixin(object):
#     """
#     * Checks whether the user is the author of the module and whether the page is
#       belong to the module, if not redirects to 'no access' view.
#     * Sets 'mymodule', 'mypage' properties to the view.
#     * Allows permission for paypal payment
#     """
#
#     def dispatch(self, request, *args, **kwargs):
#         print("module permission")
#
#         # paypal_payment = False
#         # if 'paypal_payment' in kwargs:
#         #     paypal_payment = True
#
#         if 'module_id' in kwargs:
#             try:
#                 module = StudyModule.objects.get(pk=kwargs['module_id'])
#                 self.mymodule = module
#
#                 # Select all users allowed for module
#                 mod_users = UserModule.objects.filter(module__parent=module.parent.id)
#                 allowed_users_dict = mod_users.order_by().values('user').distinct()
#                 # print("allowed_users_dict=", allowed_users_dict, '\n')
#
#                 allowed_usrs = []
#                 for usr in allowed_users_dict:
#                     allowed_usrs.append(usr['user'])
#
#                 # if paypal_payment:  # Do not check out of user
#                 #     print("paypal_payment")
#                 #     pass
#                 if request.user.id == module.user_id:
#                     pass
#                 elif request.user.id in allowed_usrs:
#                     pass
#                 else:
#                     return HttpResponseRedirect(reverse_lazy('no_access'))
#
#             except StudyModule.DoesNotExist:
#                 return HttpResponseRedirect(reverse_lazy('no_access'))
#
#         if 'page_id' in kwargs:
#             try:
#                 page = ModulePage.objects.get(pk=kwargs['page_id'])
#                 self.mypage = page
#                 self.page_type = page.type_info
#                 if page.module_id != module.id:
#                     return HttpResponseRedirect(reverse_lazy('no_access'))
#             except ModulePage.DoesNotExist:
#                 return HttpResponseRedirect(reverse_lazy('no_access'))
#         elif 'page_number' in kwargs:
#             num = int(kwargs.get('page_number', 1))
#             page = ModulePage.objects.filter(module_id=self.mymodule.id)[num - 1:num]
#             if len(page):
#                 self.mypage = page[0]
#             else:
#                 return HttpResponseRedirect(
#                     reverse_lazy('study_module_start',
#                                  kwargs={'module_id': self.mymodule.id})
#                 )
#
#         return super(ModulePermissionMixin, self).dispatch(request, *args, **kwargs)


class ModulePermissionMixin(object):
    """
    * Checks whether the user is the author of the module and whether the page is
      belong to the module, if not redirects to 'no access' view.
    * Sets 'mymodule', 'mypage' properties to the view.
    * Allows permission for paypal payment
    """

    def dispatch(self, request, *args, **kwargs):
        print("module permission")

        if 'playlist_id' in kwargs:
            try:
                playlist = PlayList.objects.get(pk=kwargs['playlist_id'])
                self.myplaylist = playlist

            except PlayList.DoesNotExist:
                return HttpResponseRedirect(reverse_lazy('no_access'))

        if 'playitem_id' in kwargs:
            try:
                playitem = PlayItem.objects.get(pk=kwargs['playitem_id'])
                self.myplayitem = playitem

            except PlayItem.DoesNotExist:
                return HttpResponseRedirect(reverse_lazy('no_access'))

        return super(ModulePermissionMixin, self).dispatch(request, *args, **kwargs)


# class StorePermissionMixin(object):
#     """
#     Checks module existence only
#     """
#     def dispatch(self, request, *args, **kwargs):
#         print("store permission")
#
#         if 'module_id' in kwargs:
#             try:
#                 self.mymodule = StudyModule.objects.get(pk=kwargs['module_id'])
#             except StudyModule.DoesNotExist:
#                 return HttpResponseRedirect(reverse_lazy('no_access'))
#
#         return super(StorePermissionMixin, self).dispatch(request, *args, **kwargs)


class AjaxHandlerMixin(object):
    """Pass ajax requests to handlers determined by 'action' parameter"""

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            if 'action' in request.POST and hasattr(self, request.POST['action']):
                handler = getattr(self, request.POST['action'])
                return handler(request)
            else:
                return HttpResponse('Action not provided or incorrect', status=400)
        else:
            return HttpResponse('Bad request', status=400)
