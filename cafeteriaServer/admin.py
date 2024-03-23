from django.contrib import admin


class CafeteriaServerAdmin(admin.AdminSite):
    site_header = 'Cafeteria Ratings Administration'
    site_title = 'Cafeteria Ratings Admin'
    index_title = 'Cafeteria Ratings Admin'
    site_url = None


cafeteriaserver_admin_site = CafeteriaServerAdmin(name='admin')
