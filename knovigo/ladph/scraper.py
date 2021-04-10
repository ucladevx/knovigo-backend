import requests
from bs4 import BeautifulSoup
import csv

# temporary
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict

from .models import Covid_HeatMap_Stats
<<<<<<< HEAD

import requests
import json


import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

=======
# get API key
from ..settings import API_KEY
>>>>>>> d45e690b8f9a67df08f44ad6d9c51ff3c5db8d83

firebase_key = "/Users/akshay/projects/helloworld/knovigo/knovigo.json"


def printCCSDB(db):
    # iterate through table
    for t in db:
        # iterate through rows in table
        for vals in t:
            # print row
            print(vals)
        # so that we can tell when one table ends and new begins
        print("_____NEW TABLE______")


# table 0 - first table of Los Angeles County Case Summary
def scrapeCountyCaseSummary(table):
    db = []
    t = []
    # iterate through city/community table
    for row in table.findAll("tr"):
        tds = row.findAll("td")
        vals = []
        for i in tds:
            vals.append(i.text)
        # if row is empty, should not consider it
        if all([i == "" for i in vals]):
            continue
        # if row starts with -, it is a subrow of whatever the previous table head was
        elif vals[0].startswith("-"):
            # print ("Table Row: " + str(vals))
            t.append(vals)

        else:
            # print ("Table Head: " + str(vals))
            db.append(t)
            t = []
            t.append(vals)
    db.append(t)
    # at the very beginning there is something with the for loop where
    # it appends an empty table
    db = db[1:]

    printCCSDB(db)
    return db


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


# table 1 - Second Table of Los Angeles County Case Summary
def scrapeCityCommunityCaseSummary(table, headerKey="th"):
    try:
        return scrapeTable(table, headerKey)
    except Exception:
        raise KeyError(
            "Error with trying to scrape the table itself from the website.")


# table 2 -
# LAC DPH Laboratory Confirmed COVID-19 Recent 14-day Cumulative
# Case and Rate per 100,000 by the Top 25 Cities/Communities
def scrapeLACDPHT25(table, headerKey="td"):
    try:
        return scrapeTable(table, headerKey)
    except Exception:
        raise KeyError(
            "Error with trying to scrape the table itself from the website.")


# table 3 - County of LA
# LAC DPH Laboratory Confirmed COVID-19 14-day Cumulative Case
# and Rate Recent Trends by City/Community1,2
def scrapeLACDPHLACounty(table, headerKey="td"):
    try:
        return scrapeTable(table, headerKey)
    except Exception:
        raise KeyError(
            "Error with trying to scrape the table itself from the website.")


# table 4 - Cities
# LAC DPH Laboratory Confirmed COVID-19 14-day Cumulative Case
# and Rate Recent Trends by City/Community1,2
def scrapeLACDPHCities(table, headerKey="th"):
    try:
        return scrapeTable(table, headerKey)
    except Exception:
        raise KeyError(
            "Error with trying to scrape the table itself from the website.")


# table 6 - NonRes Covid Counts
# Los Angeles County Non-Residential Settings Meeting the Criteria
# of Three or More Laboratory-confirmed COVID-19 Cases
def scrapeNonResCases(table, headerKey="th"):
    try:
        return scrapeTable(table, headerKey)
    except Exception:
        raise KeyError(
            "Error with trying to scrape the table itself from the website.")


# table 7 - Homeless Service Settings Covid Cases
# Los Angeles County Homeless Service Settings Meeting the Criteria
# of At Least One Laboratory-confirmed COVID-19 Case
def scrapeLACHomelessSettingCovidCases(table, headerKey="th"):
    try:
        return scrapeTable(table, headerKey)
    except Exception:
        raise KeyError(
            "Error with trying to scrape the table itself from the website.")


def scrapeLACEducationalSettingCovidCases(table, headerKey="th"):
    try:
        return scrapeTable(table, headerKey)
    except Exception:
        raise KeyError(
            "Error with trying to scrape the table itself from the website.")


# NOT IMPLEMENTED BECAUSE NOT NEEDED
def scrapeComplianceCitations(table, headerKey="td"):
    pass
    # print(table.find(div, class = ))


def heatMapDataScraper():
    url = (
        "http://publichealth.lacounty.gov/media/coronavirus/locations.htm#case-summary"
    )

    # create object by parsing the raw html content of the url and then get the list of tables
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        tables = soup.findAll("table")

    # if getting the html table contents results in an error, then somethings wrong with the site
    except:
        return (None, 1)

    # table[4] is the table called
    # LAC DPH Laboratory Confirmed COVID-19 14-day Cumulative Case and Rate Recent Trends by City/Community
    # which is what we use for the heatmap
    try:
        data = scrapeLACDPHLACounty(tables[4])

    # something went wrong with the scraping function
    except KeyError:
        return (None, 2)

    # something unknown went wrong
    except Exception:
        return (None, 3)

    # it worked!
    return (data, 0)


api_key = API_KEY


def make_id_url(place_name):
    fields = ["place_id"]
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


def get_place_id(place_name):
    url = make_id_url(place_name)
    r = requests.get(url)
    d = r.json()
    try:
        place_id = d["candidates"][0]["place_id"]
    except:
        place_id = None
        print("place id not found")
    return place_id


def construct_request(place_name, fields):
    """
            Gets Place ID of a city from Google Places API
            Sample GET Request URL:
    https://maps.googleapis.com/maps/api/place/findplacefromtext/json?
    input=Westwoord%20Los%20Angeles
    &inputtype=textquery
    &fields=place_id,geometry
    &key=hidden
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


def get_id_and_coords(place_name):
    """
    Returns (place_id, latitude, longitude) of place_name
    by querying google places API
    """
    if not place_name:
        print("Bad Place Name")
        return None

    fields = ["place_id", "geometry"]
    url = construct_request(place_name, fields)
    if url == None:
        print("Bad parameters to construct Google Places Request")
        return None

    r = requests.get(url)
    d = r.json()
    if not d or "status" not in d or d["status"] != "OK":
        print("Bad Request to Google Places: " + str(place_name))
        return None
    try:
        coords = d["candidates"][0]["geometry"]["location"]
        lat, lng = coords["lat"], coords["lng"]
        place_id = d["candidates"][0]["place_id"]
    except LookupError:
        print("Error With Response from Google Places")
        return None
    except Exception:
        print("Unknown Error")
        return None

    d = dict()
    d["id"] = place_id
    d["lat"] = lat
    d["lng"] = lng
    return d


def create_instance(lst):
    """
    Function creates dict() for a LADPH_CCDB instance from a list of data values
    lst is a list of datas for a specific city:
    [City Name, Cases, Crude Case Rate, Adjusted Case Rate, Unstable Adjusted Rate, 2018 PEPS Pop.]
    """
    if len(lst) != 6:
        return None

    city_name, cases, CCR, ACR, UAR, PEPS = lst

    place_info = get_id_and_coords(city_name)
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


def store_data(data):

    for row in data:
        if not row:
            continue

        # creates a dictionary mapping a key to every value in the row
        try:
            d = create_instance(row)
        except Exception as e:
            print(e)
            print("This Place Could Not Be Found: " + str(row[0]))
            continue
        if not d:
            continue
        print(d["place_name"])

        # update the model if it exists
        try:
            obj = Covid_HeatMap_Stats.objects.get(pk=d["place_id"])
            for (key, val) in d.items():
                setattr(obj, key, val)
            try:
                obj.save()
            except:
                print("Following Place Storage Failed: ")
                print(d["place_name"])

        except ObjectDoesNotExist:
            print(row)
            try:
                obj = Covid_HeatMap_Stats(**d)
                obj.save()
            except Exception:
                print("Following Place Storage Failed: ")
                print(d["place_name"])


def get_city_collection():
    db = firestore.client()
    if not firebase_admin._apps:
        cred = credentials.Certificate(firebase_key)
    firebase_admin.initialize_app(cred)

    collection = db.collection(u'cities3').stream()
    for doc in collection:
        print(f'{doc.id} => {doc.to_dict()}')


def load_heatmap_data(request=None):
    data, status = heatMapDataScraper()

    if status == 0:
        # load into django
        store_data(data)
        try:
            pass
        except KeyError:
            print("ERROR WITH FUNCTION: FAILED LOADING HEATMAP DATA INTO DJANGO")
        except Exception:
            print("UNKNOWN ERROR: FAILED LOADING HEATMAP DATA INTO DJANGO")
    elif status == 1:
        print("SOMETHING WRONG WITH WEBSITE")
    elif status == 2:
        print("SOMETHINGS WRONG WITH SCRAPING FUNCTION")
    elif status == 3:
        print("SOMETHING UNKNOWN WITH SCRAPING")
    return JsonResponse({"SUCCESS": True})


def get_heatmap_data(request):
    """
    return JsonResponse(
        [
            {
                "lat": 34.0635,
                "lng": -118.4455,
                "intensity": 715,
            },
            {
                "lat": 34.0913,
                "lng": -118.2936,
                "intensity": 973,
            },
        ],
        safe=False,
    )
    """

    # order is Los Angeles - Westwood, Los Angeles - East Hollywood,
    # intensity is Crude Case Rate
    if request.method == "GET":
        data = Covid_HeatMap_Stats.objects.all()
        responseData = []
        for i in data:
            djData = model_to_dict(i)
            d = dict()
            d["lat"] = djData["latitude"]
            d["lng"] = djData["longitude"]
            d["intensity"] = djData["crude_case_rate"]
            responseData.append(d)
        return JsonResponse(responseData, safe=False)
    else:
        return JsonResponse("ERROR: NOT A GET REQUEST")


if __name__ == "__main__":
    data, status = heatMapDataScraper()
    # print(status)
    # [print(i) for i in data]
    # print(get_id_and_coords("Westwood"))
