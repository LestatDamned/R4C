from django.urls import path

from .views import create_robot

urlpatterns = [
    path('api/create_robot/', create_robot),
]
