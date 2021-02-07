from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers

from . import views, scraper

router = routers.DefaultRouter()
router.register(r'places', views.PopularTimesViewSet)

# # Wire up our API using automatic URL routing.
# # Additionally, we include login URLs for the browsable API.
# urlpatterns = [
#     path('', include(router.urls)),
#     path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
# ]

urlpatterns = [
	path('all', views.place_list),
    path('filtered', views.place_filter_list),
    path('location', views.place_location_list),
    path('place/<id>', views.place_detail),
    path('get_user_report', views.get_user_report_data),
    path('get_place_data', views.get_place_data_updates),
    path('test', scraper.test_get),
]
