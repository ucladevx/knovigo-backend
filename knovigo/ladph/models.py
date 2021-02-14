from django.db import models

try:
    import requests, json
except:
    raise ImportError

api_key = "AIzaSyDdpsQ_OSZrVjRIeGoXcCXHbuG2pk1rlKI"
# Create your models here.
class LADPH_CCBCC_Manager(models.Manager):
    def construct_request(self, place_name, fields):
        """
                Gets Place ID of a city from Google Places API
                Sample GET Request URL:
        https://maps.googleapis.com/maps/api/place/findplacefromtext/json?
        input=Westwoord%20Los%20Angeles
        &inputtype=textquery
        &fields=place_id,geometry
        &key=AIzaSyDdpsQ_OSZrVjRIeGoXcCXHbuG2pk1rlKI
                returns (place_id, latitude, longitude)
        """
        if isinstance(place_name, str) and len(place_name) != 0:
            input_type = "textquery"
            name = ""
            for i in place_name:
                if i == " ":
                    name += "%20"
                else:
                    name += i

            url = (
                "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?"
                + "input="
                + name
                + "&inputtype="
                + input_type
            )
            url += "&fields="
            for f in fields:
                url += f + ","
            # we can't have the fields argument end with a comma
            if url.endswith(","):
                url = url[:-1]
            url += "&key="
            url += api_key
            return url
        return None

    def get_id_and_coords(self, place_name):
        """
        Returns (place_id, latitude, longitude) of place_name
        by querying google places API
        """
        fields = ["place_id", "geometry"]
        url = self.construct_request(place_name, fields)
        if url == None:
            return None

        r = requests.get(url)
        d = r.json()
        if not d or "status" not in d or d["status"] != "OK":
            return None

        coords = d["candidates"][0]["geometry"]["location"]
        lat, lng = coords["lat"]["lng"]
        place_id = d["candidates"][0]["place_id"]

        return (place_id, lat, lng)

    def create_instance(self, lst):
        """
        Function creates LADPH_Confirmed_Covid_By_City_Community instance from a list of data values
        lst is a list of datas for a specific city:
        [City Name, Cases, Crude Case Rate, Adjusted Case Rate, Unstable Adjusted Rate, 2018 PEPS Pop.]
        """
        if len(lst) != 6:
            return None

        city_name, cases, CCR, ACR, UAR, PEPS = lst
        id = self.get_id(city_name)
        if id == None:
            return None

        vals = get_coords(place_name)
        if not vals:
            return None

        id, lati, longi = val

        if status == 1:
            raise None

        city_data = self.create(
            place_id=id,
            place_name=city_name,
            total_cases=cases,
            latitude=lati,
            longitude=longi,
            crude_case_rate=CCR,
            adjusted_case_rate=ACR,
            unstable_adjusted_rate=UAR,
            peps_population=PEPS,
        )
        return city_data


class LADPH_Confirmed_Covid_By_City_Community(models.Model):
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
    # links this to a manager for creating instances of this class
    objects = LADPH_CCBCC_Manager()
