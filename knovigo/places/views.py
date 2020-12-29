from django.shortcuts import render # need?
from django.http import JsonResponse # need ?

# manually trigger user report scrape (can probably delete later)
from .report_scraper import scrape_user_report_data

from rest_framework import viewsets

from .serializers import PlaceSerializer
from .models import Place


# class PlaceViewSet(viewsets.ModelViewSet):
#     queryset = Place.objects.all().order_by('name')
#     serializer_class = PlaceSerializer

def places_list(request):
    """
    List all places
    """
    if request.method == 'GET':
        places = Place.objects.all()
        serializer = PlaceSerializer(places, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)

        # types, data!!

def places_filter_list(request, filter):
	"""
	List all places - ratings, name, distance, expensiveness, types, safety data
	Add location stuff!
	"""
	if request.method == 'GET':
		fields = ("google_place_id", "address", "name", "rating", "rating_n", "price_level", "types", "x_coordinate", "y_coordinate", "agg_density", "agg_social", "agg_mask")
		if filter not in fields:
			return
			# error handling
		places = Place.objects.all().only(*fields).order_by(filter)
		serializer = PlaceSerializer(places, many=True, context={'request': request}, fields = fields)
		return JsonResponse(serializer.data, safe=False)

        # types, data!!

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
      
def get_user_report_data(request):
    count = scrape_user_report_data()
    return JsonResponse({'count': count})

