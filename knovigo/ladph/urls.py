from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers

from . import views, scraper

router = routers.DefaultRouter()


urlpatterns = [
    path("heatmap", scraper.get_heatmap_data),
]