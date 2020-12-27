from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
#router.register(r'places', views.PlaceViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
# urlpatterns = [
#     path('', include(router.urls)),
#     path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
# ]

urlpatterns = [
    path('place/', views.places_list),
    path('place/<int:pk>/', views.place_detail),
    path('get_user_report', views.get_user_report_data),
] 
