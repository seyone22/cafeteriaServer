from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import ReviewViews

urlpatterns = [
    path('reviews', csrf_exempt(ReviewViews.as_view()))
]
