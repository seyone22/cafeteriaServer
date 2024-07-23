import logging
from datetime import datetime, timedelta

from django.contrib import admin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.db.models import Avg
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.timezone import make_aware
from rest_framework.authtoken.models import Token
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from cafeteriaServer.admin import cafeteriaserver_admin_site
from .actions import export_reviews_as_csv, send_email_to_recipients
from .forms import EmailConfigForm
from .models import Review, EmailConfig, Recipient
from django.utils.translation import gettext_lazy as _


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_staff')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class ReviewAdmin(admin.ModelAdmin):
    actions = [export_reviews_as_csv]
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
        yesterday = today - timedelta(days=1)
        one_week_ago = today - timedelta(days=7)

        reviews_today = Review.objects.filter(date__date=today)
        reviews_yesterday = Review.objects.filter(date__date=yesterday)
        reviews_this_week = Review.objects.filter(date__date=one_week_ago)

        avg_rating_today = reviews_today.aggregate(avg_rating=Avg('rating'))['avg_rating']
        avg_rating_yesterday = reviews_yesterday.aggregate(avg_rating=Avg('rating'))['avg_rating']
        avg_rating_this_week = reviews_this_week.aggregate(avg_rating=Avg('rating'))['avg_rating']

        log_value = (Review.objects.filter(site="MAIN")).aggregate(avg_rating=Avg('rating'))['avg_rating']

        context = {
            'title': 'Review Statistics',
            'avg_rating_today': avg_rating_today,
            'avg_rating_yesterday': avg_rating_yesterday,
            'avg_rating_this_week': avg_rating_this_week,
            'log_value': log_value
        }

        return TemplateResponse(request, 'admin/review_statistics.html', context)


class TokenAdmin(admin.ModelAdmin):
    list_display = ['key', 'user']


class UserAdmin(BaseUserAdmin):  # Corrected
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ['username', 'email', 'is_staff', 'is_superuser']  # Corrected
    actions = ['generate_tokens']

    def generate_tokens(self, request, queryset):
        for user in queryset:
            token, created = Token.objects.get_or_create(user=user)
        self.message_user(request, "Tokens generated successfully for selected users.")

    generate_tokens.short_description = "Generate Tokens"


class EmailConfigAdmin(admin.ModelAdmin):
    form = EmailConfigForm
    list_display = ('smtp_server', 'smtp_port', 'sender_email', 'send_time', 'email_subject')
    fieldsets = (
        ('Email Configuration', {
            'fields': ('smtp_server', 'smtp_port', 'sender_email', 'send_time', 'email_subject', 'email_body', 'smtp_username', 'smtp_password'),
        }),
    )

    readonly_fields = ('smtp_password',)  # Ensure password is read-only

    def send_test_email(self, request, queryset):
        if queryset.exists():
            email_config = queryset.first()

            subject = "Test Email"
            message = "This is a test email to verify your email configuration."
            from_email = email_config.sender_email
            recipient_list = [email_config.sender_email]

            try:
                send_mail(subject, message, from_email, recipient_list)
                self.message_user(request, _("Test email sent successfully."))
            except Exception as e:
                self.message_user(request, _("Failed to send test email: %s" % str(e)), level=admin.ERROR)

    send_test_email.short_description = "Send Test Email"

    actions = [send_test_email]
    def has_add_permission(self, request):
        # Disable the ability to add more instances via the admin interface
        return EmailConfig.objects.count() == 0

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion via the admin interface
        return False

    def get_queryset(self, request):
        # Limit queryset to only the existing instance
        qs = super().get_queryset(request)
        return qs.filter(pk=1)

    def has_change_permission(self, request, obj=None):
        # Restrict change permission to only allow editing the existing instance
        return obj is not None


class RecipientAdmin(admin.ModelAdmin):
    list_display = ['email_address']
    actions = [send_email_to_recipients]  # Add the custom action here


# Register the Review model
cafeteriaserver_admin_site.register(Review, ReviewAdmin)

# Register the Token model
cafeteriaserver_admin_site.register(Token, TokenAdmin)

# Register the User and Group models
cafeteriaserver_admin_site.register(User, UserAdmin)
cafeteriaserver_admin_site.register(Group)

# Register the EmailConfig model
cafeteriaserver_admin_site.register(EmailConfig, EmailConfigAdmin)

# Register the recipient model
cafeteriaserver_admin_site.register(Recipient, RecipientAdmin)
