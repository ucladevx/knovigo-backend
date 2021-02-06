from django.db import models

# Create your models here.


class LACDPH_Confirmed_Covid_By_City_Community(models.Model):
    # https://developers.google.com/places/web-service/search refer to this for place id
    # the api key is in places/scraper.py
    place_id = models.CharField(primary_key=True, max_length=100)
    # city or community name
    place_name = models.CharField(max_length=50)
    # latitude/longitude of place
    latitude = models.FloatField()
    longitude = models.FloatField()
    # out of 100,000 according to most recent version of website 1/23/2021
    crude_case_rate = models.IntegerField()
    adjusted_case_rate = models.IntegerField()
    # in the table, its either blank or a ^ indicating unstable
    unstable_case_rate = models.CharField(max_length=50)
    peps_population = models.IntegerField()
