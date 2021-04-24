from django.urls import path, register_converter
from django.conf.urls import url, include
from rest_framework import routers

from . import converters, views, scraper

router = routers.DefaultRouter()
router.register(r'places', views.PopularTimesViewSet)
register_converter(converters.FloatUrlParameterConverter, 'float')
# # Wire up our API using automatic URL routing.
# # Additionally, we include login URLs for the browsable API.
# urlpatterns = [
#     path('', include(router.urls)),
#     path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
# ]

urlpatterns = [
	path('all', views.place_list),
    path('filtered', views.place_filter_list),
    path('location/<float:latitude>/<float:longitude>', views.place_location_list),
    path('place/<id>', views.place_detail),
    path('recs', views.place_busiest),
    path('get_user_report', views.get_user_report_data),
    path('get_place_data', views.get_place_data_updates),
    path('save_app_report', views.save_app_report),
    path('test', scraper.test_get),
]
