from django.urls import path

from .views import create_robot, create_robot_report

urlpatterns = [
    path('create_robot/', create_robot),
    path('create_report/', create_robot_report)
]
