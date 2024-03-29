from django.db import models
try:
    import requests
    import json
except:
    raise ImportError


class Covid_HeatMap_Stats(models.Model):
    # https://developers.google.com/places/web-service/search refer to this for place id
    # the api key is in places/scraper.py

    place_id = models.CharField(primary_key=True, max_length=100)
    place_name = models.CharField(max_length=50)
    total_cases = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    # out of 100,000 according to most recent version of website 1/23/2021
    crude_case_rate = models.IntegerField()
    adjusted_case_rate = models.IntegerField()
    # in the table, unstable case rate either blank or a ^ indicating unstable
    unstable_adjusted_rate = models.CharField(max_length=50)
    peps_population = models.IntegerField()


class city_vaccination_info(models.Model):
    place_id = models.CharField(primary_key=True, max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    place_name = models.CharField(max_length=50)
    number_vaccinated = models.IntegerField()
    percentage_vaccinated = models.FloatField()
    population = models.IntegerField()
