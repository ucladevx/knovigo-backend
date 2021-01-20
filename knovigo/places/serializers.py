# serializers.py
from rest_framework import serializers

from .models import Place
from .models import PopularTimes
from .models import BusinessHours

from geopy.distance import geodesic

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

class PlaceSerializer(DynamicFieldsModelSerializer):
	distance = serializers.SerializerMethodField('getDistance')

	def getDistance(self, obj):
		x_coord = self.context.get("x_coordinate")
		y_coord = self.context.get("y_coordinate")
		if x_coord and y_coord:
			distance = geodesic((x_coord, y_coord), (obj.x_coordinate, obj.y_coordinate)).miles
		else:
			distance = 0 # replace later !

	class Meta:
		model = Place
		fields = ('__all__')

class PopularTimesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PopularTimes
        fields = ('__all__')

class BusinessHoursSerializer(serializers.ModelSerializer):
	class Meta:
		model = BusinessHours
		fields = ('__all__')