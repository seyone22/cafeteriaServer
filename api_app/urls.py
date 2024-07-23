from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views
from .views import ReviewViews, email_config_view

urlpatterns = [
    path('reviews', csrf_exempt(ReviewViews.as_view())),
    path('send-email/', views.send_email_view, name='send_email'),
]
