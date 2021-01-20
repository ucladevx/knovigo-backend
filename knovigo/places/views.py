from django.shortcuts import render # need?
from django.http import JsonResponse # need ?

# manually trigger user report scrape (can probably delete later)
from .report_scraper import scrape_user_report_data

from rest_framework import viewsets

from .serializers import PlaceSerializer
from .models import Place
from .serializers import BusinessHoursSerializer
from .models import BusinessHours
from .serializers import PopularTimesSerializer
from .models import PopularTimes


# class PlaceViewSet(viewsets.ModelViewSet):
#     queryset = Place.objects.all().order_by('name')
#     serializer_class = PlaceSerializer

# class BusinessHoursViewSet(viewsets.ModelViewSet):
#     queryset = BusinessHours.objects.all()
#     serializer_class = BusinessHoursSerializer

# class PopularTimesViewSet(viewsets.ModelViewSet):
#     queryset = PopularTimes.objects.all()
#     serializer_class = PopularTimesSerializer


def place_detail(request, id):
    """
    Get details for a place
    """
    try:
        place = Place.objects.get(google_place_id=id)
    except Place.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PlaceSerializer(place)
        return JsonResponse(serializer.data)

def place_location_list(request, location):
	"""
	List all places - ratings, name, distance, expensiveness, types, safety data
	"""
	if request.method == 'GET':
		fields = ("google_place_id", "address", "name", "hours", "rating", "rating_n", "price_level", "types", "x_coordinate", "y_coordinate", "agg_density", "agg_social", "agg_mask", "distance")
		places = Place.objects.all().only(*fields).order_by("distance") # refine order by filter with more data
		serializer = PlaceSerializer(places, many=True, context={'request': request}, fields = fields)
		return JsonResponse(serializer.data, safe=False)

def place_filter_list(request):
	"""
	List all places with basic information
	"""
	if request.method == 'GET':
		fields = ("google_place_id", "address", "name", "hours", "rating", "rating_n", "price_level", "types", "x_coordinate", "y_coordinate", "agg_density", "agg_social", "agg_mask", "distance")
		places = Place.objects.all().only(*fields).order_by(filter) # refine order by filter with more data
		serializer = PlaceSerializer(places, many=True, context={'request': request}, fields = fields)
		return JsonResponse(serializer.data, safe=False)

def place_list(request, location):
    """
    List all places with all information
    """
    if request.method == 'GET':
        places = Place.objects.all()
        serializer = PlaceSerializer(places, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)
      
def get_user_report_data(request):
    count = scrape_user_report_data()
    return JsonResponse({'count': count})

