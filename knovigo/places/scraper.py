import populartimes
import requests
from collections import defaultdict
from django.core.exceptions import ObjectDoesNotExist

from .models import Place, PopularTimes, BusinessHours

# temporary
from django.http import JsonResponse

WESTWOOD_LOCATIONS = [
    "ChIJM2_CO4G8woARCvO-wn-MObo",  # Westwood Target
    "ChIJDepxE4G8woAR4BETlQXlSt8",  # Westwood Trader Joe's
    "ChIJU9RXX4G8woARM6tDKbo-o40",  # Westwood CVS
    "ChIJf5fVvoO8woARChfRh6MOi8o",  # Westwood Whole Foods
    "ChIJz3nnNoG8woARM2mO30LUT-Q",  # Westwood Ralph's
    "ChIJ9bElwYO8woARyFBerBC6aRs",  # Westwood Barney's Beanery
    "EidKYW5zcyBTdGVwcywgTG9zIEFuZ2VsZXMsIENBIDkwMDk1LCBVU0EiLiosChQKEgmP7FgEibzCgBGSTtcJJ1JtZhIUChIJE9on3F3HwoAR9AhGJW_fL-I",  # Tongva steps
    "ChIJD28uC4S8woARUk1Z5qNqmjk",  # Westwood Diddy Riese
    "ChIJSXU3ioO8woARK-IVICYTrVI",  # BJ's Restaurant and Brewery
]

# TODO don't hardcode this
api_key = "AIzaSyDdpsQ_OSZrVjRIeGoXcCXHbuG2pk1rlKI"


# TODO fix this
def get_place_data(place_id):
    # modify the fields we retrieve
    # do we rely more on the populartimes call to reduce redundant
    fields = "website,opening_hours,photos,price_level"
    response = requests.get(
        "https://maps.googleapis.com/maps/api/place/details/json?place_id=" + place_id + "&fields=" + fields + "&key=" + api_key)
    print(response.json())


def update_place_model(place_id):
    # get popular times stuff!
    d = defaultdict(str, populartimes.get_id(api_key, place_id))
    name = d['name']
    address = d['address']
    types = d['types']
    latitude = d['coordinates']['lat']
    longitude = d['coordinates']['lng']
    rating = d['rating']
    rating_n = d['rating_n']

    try:
        place_model = Place.objects.get(pk=place_id)
        place_model.name = name
        place_model.address = address
        place_model.latitude = latitude
        place_model.rating = rating
        place_model.rating_n = rating_n
    except ObjectDoesNotExist:
        place_model = Place(place_id=place_id, name=name, address=address, types=types, latitude=latitude,
                            longitude=longitude, rating=rating, rating_n=rating_n, agg_density=0,
                            agg_density_n=0, agg_social=0, agg_social_n=0, agg_mask=0, agg_mask_n=0,
                            covid_updates=None, confirmed_staff_infected=-1)

    monday = d['populartimes'][0]['data']
    tuesday = d['populartimes'][1]['data']
    wednesday = d['populartimes'][2]['data']
    thursday = d['populartimes'][3]['data']
    friday = d['populartimes'][4]['data']
    saturday = d['populartimes'][5]['data']
    sunday = d['populartimes'][6]['data']
    try:
        pt_model = place_model.populartimes
        pt_model.monday = monday
        pt_model.tuesday = tuesday
        pt_model.wednesday = wednesday
        pt_model.thursday = thursday
        pt_model.friday = friday
        pt_model.saturday = saturday
        pt_model.sunday = sunday
    except ObjectDoesNotExist:
        pt_model = PopularTimes(place=place_model, monday=monday, tuesday=tuesday, wednesday=wednesday,
                                thursday=thursday, friday=friday, saturday=saturday, sunday=sunday)

    place_model.save()
    pt_model.save()


def update_place_data():
    # temporary (later, iterate through all locations)
    update_place_model(WESTWOOD_LOCATIONS[0])


def test_get(request):
    # test - get place data for Target
    place_id = WESTWOOD_LOCATIONS[0]
    try:
        place_model = Place.objects.get(pk=place_id)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'place model not found'})
    try:
        pt_model = place_model.populartimes
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'populartimes not found'})

    return JsonResponse({'id': place_model.place_id, 'name': place_model.name, 'monday': pt_model.monday})
