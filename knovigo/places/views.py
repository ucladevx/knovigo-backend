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
        serializer = PlaceSerializer(places, many=True)
        return JsonResponse(serializer.data, safe=False)

def place_detail(request, pk):
    """
    Get details for a place
    """
    try:
        place = Place.objects.get(pk=pk)
    except Place.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PlaceSerializer(place)
        return JsonResponse(serializer.data)
      
def get_user_report_data(request):
    count = scrape_user_report_data()
    return JsonResponse({'count': count})

