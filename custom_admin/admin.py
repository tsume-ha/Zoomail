from django.contrib import messages
from django.contrib.admin import AdminSite
from django.shortcuts import render

class CustomAdminSite(AdminSite):
    site_header = 'Zoomail 管理者用サイト'
    def password_change(self, request, extra_context=None):
        """
        Handle the "change password" task -- both form display and validation.
        """
        # from django.contrib.admin.forms import AdminPasswordChangeForm
        # from django.contrib.auth.views import PasswordChangeView
        # url = reverse('admin:password_change_done', current_app=self.name)
        # defaults = {
        #     'form_class': AdminPasswordChangeForm,
        #     'success_url': url,
        #     'extra_context': {**self.each_context(request), **(extra_context or {})},
        # }
        # if self.password_change_template is not None:
        #     defaults['template_name'] = self.password_change_template
        # request.current_app = self.name
        
        messages.error(request, 'Zoomailではパスワードを設定しません')

        return render(request, 'registration/password_change_form.html')


        
custom_admin_site = CustomAdminSite(name='custom_admin')
