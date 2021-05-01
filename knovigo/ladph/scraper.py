import requests
from bs4 import BeautifulSoup
import csv

# temporary
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict

# from .models import Covid_HeatMap_Stats
from .models import city_vaccination_info

import requests
import json


import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


firebase_key = "./knovigofirebase.json"


def scrapeTable(table, headerKey):
    # gets the label of each column from table head
    thead = table.find("thead")
    db = []
    head = []
    for header in thead:
        tds = header.findAll(headerKey)
        for i in tds:
            head.append(i.text)

    # gets the the rest of the data from the actual table rows
    db.append(head)
    for row in table.findAll("tr"):
        tds = row.findAll("td")
        data = []
        for i in tds:
            data.append(i.text)
        db.append(data)
    db.pop(1)
    return db


# table 2 -
# LAC DPH Laboratory Confirmed COVID-19 Recent 14-day Cumulative
# Case and Rate per 100,000 by the Top 25 Cities/Communities
def scrapePercentVaccinated(table, headerKey="td"):
    try:
        return scrapeTable(table, headerKey)
    except Exception:
        raise KeyError(
            "Error with trying to scrape the table itself from the website.")


def heatMapDataScraper():
    url = (
        "http://publichealth.lacounty.gov/media/coronavirus/locations.htm#case-summary"
    )

    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        tables = soup.findAll("table")

    except:
        return (None, 1)

    if not tables:
        return (None, 2)

    try:
        data = scrapePercentVaccinated(tables[2])

    except KeyError:
        return (None, 3)

    except Exception:
        return (None, 4)

    return (data, 0)


def get_id_and_coords(place_name, city_data):
    """
    Returns (place_id, latitude, longitude) of place_name
    by querying google places API
    """
    if not place_name:
        print("Bad Place Name")
        return None

    # we replace all / with _ to store in firebase's city_data
    formatted_place_name = place_name.replace("/", "_")
    # if we do have the place in our firebase db, get the data and return it
    if formatted_place_name in city_data:
        d = dict()
        d["id"] = city_data[formatted_place_name]["place_id"]
        d["lat"] = city_data[formatted_place_name]["latitude"]
        d["lng"] = city_data[formatted_place_name]["longitude"]
        return d
    else:
        print(f'{formatted_place_name} not in Firebase')
        return None


def create_covid_data_instance(lst, city_data):
    """
    Function creates dict() for a LADPH_CCDB instance from a list of data values
    lst is a list of datas for a specific city:
    [City Name, Cases, Crude Case Rate, Adjusted Case Rate, Unstable Adjusted Rate, 2018 PEPS Pop.]
    """
    print(lst)
    if len(lst) != 6:
        print("here2")
        return None

    city_name, cases, CCR, ACR, UAR, PEPS = lst

    place_info = get_id_and_coords(city_name, city_data)
    # print("place_info", place_info)
    if not place_info:
        return None

    d = dict()

    d["place_id"] = place_info["id"]
    d["place_name"] = city_name
    d["total_cases"] = cases
    d["latitude"] = place_info["lat"]
    d["longitude"] = place_info["lng"]
    d["crude_case_rate"] = CCR
    d["adjusted_case_rate"] = ACR
    d["unstable_adjusted_rate"] = UAR
    d["peps_population"] = PEPS
    return d


def create_vaccine_data_instance(lst, city_data):
    '''
    function creates a city_vaccination_info dictionary 
    for a given lst with 
    [city/community name, number of people vaccinated, population, percentage of people vaccinated]
    '''
    if len(lst) != 4:
        print("Bad list format given")
        return None

    city_name, number_vaccinated, population, percentage_vaccinated = lst

    place_info = get_id_and_coords(city_name, city_data)
    if not place_info:
        return None

    d = dict()
    try:
        d["place_id"] = place_info["id"]
        d["latitude"] = place_info["lat"]
        d["longitude"] = place_info["lng"]
    except KeyError:
        return None

    d["place_name"] = city_name
    d["number_vaccinated"] = number_vaccinated
    d["population"] = population
    d["percentage_vaccinated"] = percentage_vaccinated

    return d


def store_data(data, city_data):

    for row in data:
        if not row:
            continue

        # creates a dictionary mapping a key to every value in the row
        try:
            d = create_vaccine_data_instance(row, city_data)
        except Exception as e:
            print(e)
            print("This Place Could Not Be Found: " + str(row[0]))
            continue
        if not d:
            continue

        print(d["place_name"])

        # update the model if it exists
        try:
            obj = city_vaccination_info.objects.get(pk=d["place_id"])
            for (key, val) in d.items():
                setattr(obj, key, val)
            try:
                obj.save()
            except:
                print("Following Place Storage Failed: ")
                print(d["place_name"])

        except ObjectDoesNotExist:
            try:
                obj = city_vaccination_info(**d)
                obj.save()
            except Exception as e:
                print(f'Following Place Storage Failed: {e}')
                print(d["place_name"])


def get_city_collection():
    '''
    gets a stream of data from the cities3 collection
    which has the latitude, longitude, place id of a given 
    city_name
    '''

    if not firebase_admin._apps:
        cred = credentials.Certificate(firebase_key)
        firebase_admin.initialize_app(cred)

    db = firestore.client()

    collection = db.collection(u'cities3').stream()
    city_data = dict()
    for doc in collection:
        city_data[doc.id] = doc.to_dict()

    return city_data


def load_heatmap_data(request=None):
    data, status = heatMapDataScraper()
    city_data = get_city_collection()
    if status == 0:
        # load into django
        try:
            store_data(data, city_data)
            return JsonResponse({"SUCCESS": True})
        except KeyError:
            print("ERROR WITH FUNCTION: FAILED LOADING HEATMAP DATA INTO DJANGO")
        except Exception:
            print("UNKNOWN ERROR: FAILED LOADING HEATMAP DATA INTO DJANGO")
    elif status == 1:
        print("SOMETHING WRONG WITH WEBSITE")
    elif status == 2:
        print("NO TABLES SCRAPED")
    elif status == 3:
        print("SOMETHING WRONG WITH HTML OF TABLES RETRIEVED")
    elif status == 4:
        print("SOMETHING UNKNOWN WRONG WITH SCRAPING SITE")

    return JsonResponse({"SUCCESS": False})


def get_heatmap_data(request):
    if request.method == "GET":
        data = city_vaccination_info.objects.all()
        responseData = []
        for i in data:
            djData = model_to_dict(i)
            d = dict()
            d["lat"] = djData["latitude"]
            d["lng"] = djData["longitude"]
            d["intensity"] = 100 - djData["percentage_vaccinated"]
            responseData.append(d)
        return JsonResponse(responseData, safe=False)
    else:
        return JsonResponse("ERROR: NOT A GET REQUEST")


def show_db(request):
    '''
    Just a method for viewing the contents of the database
    '''
    if request.method == "GET":
        data = city_vaccination_info.objects.all()
        responseData = []
        for i in data:
            djData = model_to_dict(i)
            responseData.append(djData)
        return JsonResponse(responseData, safe=False)
    else:
        return JsonResponse("ERROR: NOT A GET REQUEST")


if __name__ == "__main__":
    data, status = heatMapDataScraper()
    [print(i) for i in data]
