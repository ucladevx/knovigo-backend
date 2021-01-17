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
    "EidKYW5zcyBTdGVwcywgTG9zIEFuZ2VsZXMsIENBIDkwMDk1LCBVU0EiLiosChQKEgmP7FgEibzCgBGSTtcJJ1JtZhIUChIJE9on3F3HwoAR9AhGJW_fL-I",
    # Tongva steps
    "ChIJD28uC4S8woARUk1Z5qNqmjk",  # Westwood Diddy Riese
    "ChIJSXU3ioO8woARK-IVICYTrVI",  # BJ's Restaurant and Brewery
]

# TODO don't hardcode this
api_key = ""


# TODO fix this
def get_place_data(place_id):
    # modify the fields we retrieve
    # do we rely more on the populartimes call to reduce redundant
    fields = "website,opening_hours,photos,price_level"
    response = requests.get(
        "https://maps.googleapis.com/maps/api/place/details/json?place_id=" + place_id + "&fields=" + fields + "&key=" + api_key)
    return response.json()


def parse_place_data(data):
    try:
        price_level = data['result']['price_level']
    except KeyError:
        print(data)
        price_level = 0

    try:
        website = data['result']['website']
    except KeyError:
        website = ""
    open_times = dict()
    # day is indexed from 0 = sunday
    try:
        for one_day_time in data['result']['opening_hours']['periods']:
            day = one_day_time['close']['day']
            close_time = one_day_time['close']['time']
            open_time = one_day_time['open']['time']
            open_interval = (open_time, close_time)
            open_times[day] = open_interval
    except KeyError:
        open_times = dict()

    if open_times != {}:
        for i in range(7):
            if i not in open_times.keys():
                open_times[i] = ('0000', '2359')

    return price_level, website, open_times


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
    phone_number = d['international_phone_number']
    if phone_number == "":
        phone_number = d['formatted_phone_number']

    if rating == "":
        rating = None
    if rating_n == "":
        rating_n = None

    place_data = get_place_data(place_id)
    expense, website, open_hours = parse_place_data(place_data)

    try:
        place_model = Place.objects.get(pk=place_id)
        place_model.name = name
        place_model.address = address
        place_model.latitude = latitude
        place_model.rating = rating
        place_model.rating_n = rating_n
        place_model.website = website
        place_model.price_level = expense
        place_model.phone_number = phone_number

    except ObjectDoesNotExist:
        place_model = Place(place_id=place_id, name=name, address=address, types=types, latitude=latitude,
                            longitude=longitude, rating=rating, rating_n=rating_n, agg_density=0,
                            agg_density_n=0, agg_social=0, agg_social_n=0, agg_mask=0, agg_mask_n=0,
                            covid_updates=None, confirmed_staff_infected=-1)
    place_model.save()

    # business hours
    if open_hours != {}:
        try:
            bz_model = place_model.businesshours
            bz_model.monday_open = open_hours[1][0]
            bz_model.monday_close = open_hours[1][1]
            bz_model.tuesday_open = open_hours[2][0]
            bz_model.tuesday_close = open_hours[2][1]
            bz_model.wednesday_open = open_hours[3][0]
            bz_model.wednesday_close = open_hours[3][1]
            bz_model.thursday_open = open_hours[4][0]
            bz_model.thursday_close = open_hours[4][1]
            bz_model.friday_open = open_hours[5][0]
            bz_model.friday_close = open_hours[5][1]
            bz_model.saturday_open = open_hours[6][0]
            bz_model.saturday_close = open_hours[6][1]
            bz_model.sunday_open = open_hours[0][0]
            bz_model.sunday_close = open_hours[0][1]

        except ObjectDoesNotExist:
            bz_model = BusinessHours(place=place_model,
                                     monday_open=open_hours[1][0], monday_close=open_hours[1][1],
                                     tuesday_open=open_hours[2][0], tuesday_close=open_hours[2][1],
                                     wednesday_open=open_hours[3][0], wednesday_close=open_hours[3][1],
                                     thursday_open=open_hours[4][0], thursday_close=open_hours[4][1],
                                     friday_open=open_hours[5][0], friday_close=open_hours[5][1],
                                     saturday_open=open_hours[6][0], saturday_close=open_hours[6][1],
                                     sunday_open=open_hours[0][0], sunday_close=open_hours[0][1])
        bz_model.save()

    if 'populartimes' in d.keys():
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
        pt_model.save()


def update_place_data():
    for location in WESTWOOD_LOCATIONS:
        update_place_model(location)
    return len(WESTWOOD_LOCATIONS)
    # update_place_model(WESTWOOD_LOCATIONS[8])


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
