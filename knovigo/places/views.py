from django.shortcuts import render # need?
from django.http import JsonResponse # need ?

from rest_framework import viewsets

from .serializers import PlaceSerializer
from .models import Place


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all().order_by('name')
    serializer_class = PlaceSerializer