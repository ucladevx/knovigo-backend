from django.http import JsonResponse, HttpResponse

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import GEOSGeometry,Point
from django.views.decorators.csrf import csrf_exempt

# manually trigger scraper functions for testing (can probably delete later)
import json
from .report_scraper import scrape_user_report_data
from .scraper import update_place_data
from .report_data_saver import save_data_from_report
from rest_framework import viewsets

from .serializers import PlaceSerializer
from .models import Place
from .serializers import BusinessHoursSerializer
from .models import BusinessHours
from .serializers import PopularTimesSerializer
from .models import PopularTimes
from geopy.distance import geodesic
from django.db.models import F

class PopularTimesViewSet(viewsets.ModelViewSet):
	queryset = PopularTimes.objects.all()
	serializer_class = PopularTimesSerializer

def place_detail(request, id):
	"""
	Get details for a place
	"""
	try:
		place = Place.objects.get(place_id=id)
	except Place.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = PlaceSerializer(place)
		return JsonResponse(serializer.data)

# Added latitude and longitude parameters. TODO: add distance calculation
def place_location_list(request, latitude, longitude):
	"""
	List all places - ratings, name, distance, expensiveness, types, safety data
	"""
	if request.method == 'GET':
		fields = ("place_id", "address", "name", "businessHours", "rating", "rating_n", "price_level", "types", "latitude", "longitude", "agg_density", "agg_social", "agg_mask", "distance", "coordinates")
		reference_point = Point(latitude, longitude, srid=4326)
		places = Place.objects.all().annotate(distance=Distance("coordinates", reference_point)).order_by("distance")
		serializer = PlaceSerializer(places, many=True, context={'request': request}, fields = fields)
		return JsonResponse(serializer.data, safe=False)

def place_filter_list(request):
	"""
	List all places with basic information
	"""
	if request.method == 'GET':
		fields = ("place_id", "address", "name", "rating", "rating_n", "price_level", "types", "latitude", "longitude", "agg_density", "agg_social", "agg_mask", "businessHours", "popularTimes")
		places = Place.objects.all().order_by("agg_density") # refine order by filter with more data
		serializer = PlaceSerializer(places, many=True, context={'request': request}, fields = fields)
		return JsonResponse(serializer.data, safe=False)

def place_list(request):
	"""
	List all places with all information
	"""
	if request.method == 'GET':
		places = Place.objects.all()
		serializer = PlaceSerializer(places, many=True, context={'request': request})
		return JsonResponse(serializer.data, safe=False)
	  
def get_place_data_updates(request):
	update_place_data()
	return JsonResponse({'success': True})

def get_user_report_data(request):
    count = scrape_user_report_data()
    return JsonResponse({'count': count})


@csrf_exempt
def save_app_report(request):
    ret_value, ret_string = save_data_from_report(request)
    if ret_value == 1:
        print("Error", ret_string)
        return JsonResponse({'success': False, 'err_msg': ret_string})
    return JsonResponse({'success': True})
