from datetime import datetime, timedelta

from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.db.models import Avg
from django.http import HttpResponse
from django.urls import path
from rest_framework.authtoken.models import Token

from cafeteriaServer.admin import cafeteriaserver_admin_site
from .models import Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['date', 'rating', 'site']
    list_filter = ['date', 'site']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('statistics/', self.statistics_view),
        ]
        return custom_urls + urls

    def statistics_view(self, request):
        today = datetime.now().date()
        one_week_ago = today - timedelta(days=7)

        reviews_today = Review.objects.filter(created_at__date=today)
        reviews_this_week = Review.objects.filter(created_at__date__gte=one_week_ago)

        avg_rating_today = reviews_today.aggregate(avg_rating=Avg('rating'))['avg_rating']
        avg_rating_this_week = reviews_this_week.aggregate(avg_rating=Avg('rating'))['avg_rating']

        content = f'<h1>Review Statistics</h1>'
        content += f'<p>Average rating today: {avg_rating_today}</p>'
        content += f'<p>Average rating this week: {avg_rating_this_week}</p>'

        return HttpResponse(content)


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
