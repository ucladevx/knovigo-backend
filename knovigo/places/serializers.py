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

    For nested fields: Use the name of the nested field to include it
    For reference: https://stackoverflow.com/questions/35036262/django-rest-framework-nested-serializer-dynamic-model-fields
    """
    def __init__(self, *args, **kwargs):

        def parse_nested_fields(fields):
            field_object = {"fields": []}
            for f in fields:
                obj = field_object
                nested_fields = f.split("__")
                for v in nested_fields:
                    if v not in obj["fields"]:
                        obj["fields"].append(v)
                    if nested_fields.index(v) < len(nested_fields) - 1:
                        obj[v] = obj.get(v, {"fields": []})
                        obj = obj[v]
            return field_object

        def select_nested_fields(serializer, fields):
            for k in fields:
                if k == "fields":
                    fields_to_include(serializer, fields[k])
                else:
                    select_nested_fields(serializer.fields[k], fields[k])

        def fields_to_include(serializer, fields):
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(serializer.fields.keys())
            for field_name in existing - allowed:
                serializer.fields.pop(field_name)

        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)
        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            fields = parse_nested_fields(fields)
            # Drop any fields that are not specified in the `fields` argument.
            select_nested_fields(self, fields)

class PopularTimesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PopularTimes
        fields = ('__all__')

class BusinessHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessHours
        fields = ('__all__')

class PlaceSerializer(DynamicFieldsModelSerializer):
    businessHours = serializers.SerializerMethodField()
    popularTimes = serializers.SerializerMethodField()

    class Meta:
        model = Place
        fields = ('__all__')

    def get_businessHours(self, obj):
        "obj is a Place instance. Returns list of dicts"""
        qset = BusinessHours.objects.filter(place=obj)
        return [BusinessHoursSerializer(m).data for m in qset]

    def get_popularTimes(self, obj):
        "obj is a Place instance. Returns list of dicts"""
        qset = PopularTimes.objects.filter(place=obj)
        return [PopularTimesSerializer(m).data for m in qset]
