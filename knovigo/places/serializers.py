# serializers.py
from rest_framework import serializers

from .models import Place

class PlaceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Place
        fields = ('google_place_id', 'name', 'address', #'types', 
        	'x_coordinate', 
        	'y_coordinate', 'rating', 'rating_n', 'phone_number', 'website', 'icon', 
        	'price_level', 
        	#'covid_updates', 
        	'confirmed_staff_infected',  'agg_density', 'agg_density_n', 'agg_social',
    		'agg_social_n', 'agg_mask', 'agg_mask_n', 'created_at', 'updated_at')

	#handle hours and popular times