from django.urls import path

from . import views

urlpatterns = [
    path('get_user_report', views.get_user_report_data),
] 