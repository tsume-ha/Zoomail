from django.contrib.admin import AdminSite

class CustomAdminSite(AdminSite):
    site_header = 'Zoomail 管理者用サイト'

admin_site = CustomAdminSite(name='custom_admin')

