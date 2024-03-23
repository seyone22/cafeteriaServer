from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from .models import Review
from cafeteriaServer.admin import cafeteriaserver_admin_site
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User, Group


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['date', 'rating', 'site']
    list_filter = ['date', 'site']


class TokenAdmin(admin.ModelAdmin):
    list_display = ['key', 'user']


class UserAdmin(admin.ModelAdmin):  # Corrected
    list_display = ['username', 'email', 'is_staff', 'is_superuser']  # Corrected
    actions = ['generate_tokens']

    def generate_tokens(self, request, queryset):
        for user in queryset:
            token, created = Token.objects.get_or_create(user=user)
        self.message_user(request, "Tokens generated successfully for selected users.")

    generate_tokens.short_description = "Generate Tokens"


# Register the Review model
cafeteriaserver_admin_site.register(Review, ReviewAdmin)

# Register the Token model
cafeteriaserver_admin_site.register(Token, TokenAdmin)

# Register the User and Group models
cafeteriaserver_admin_site.register(User, UserAdmin)
cafeteriaserver_admin_site.register(Group)
