from django.urls import path
from .views import ReviewViews

urlpatterns = [
    path('reviews/', ReviewViews.as_view())
]