# merge this with scraper.py later

import urllib.request
import csv
from datetime import datetime
from io import StringIO
from dateutil import parser
from .models import UserReport
from .models import Place
from .scraper import WESTWOOD_LOCATIONS

def scrape_user_report_data():
    if len(UserReport.objects.filter(from_google_form=True)) == 0:
        timefilter = parser.parse("01/01/2000 00:00:00 -0800")
    else:
        timefilter = UserReport.objects.filter(from_google_form=True).order_by("-created").first().created

    with urllib.request.urlopen(
            'https://docs.google.com/spreadsheets/d/1fJ4hGyMX1wqMs6G9tA5wcogKWj29QY73iQ-r5SG74V4/gviz/tq?tqx=out:csv') as f:
        raw_csv = f.read().decode('utf-8')
    file = StringIO(raw_csv)
    reader = csv.reader(file, delimiter=',')
    # skip header row
    next(reader)
    percents_dict = {'0 - 25%': 0, '25 - 50%': 1, '50 - 75%': 2, '75 - 100%': 3}

    count = 0
    for row in reader:
        timestamp = parser.parse(row[0] + " -0800")
        if timestamp <= timefilter:
            continue
        daystring = timestamp.strftime("%m/%d/%Y ")
        place = row[1]

        # try to the corresponding place id for the place chosen
        try:
            place_id = WESTWOOD_LOCATIONS[place]
        except KeyError:
            place_id = "Other"

        start = parser.parse(daystring + row[2] + " -0800")
        end = parser.parse(daystring + row[3] + " -0800")
        social_distancing = percents_dict[row[4]]
        mask_wearing = percents_dict[row[5]]
        crowded = percents_dict[row[6]]
        covid_notes = row[7]
        covid_protocol = int(row[8])
        other_comments = row[9]

        if row[11] == '':
            # before this data was collected
            masks_required_checkbox = 2
            staff_masks_checkbox = 2
            plexiglass_checkbox = 2
            line_outside_checkbox = 2
            capacity_checkbox = 2
            takeout_checkbox = 2
            dine_in_checkbox = 2
            outdoor_seating_checkbox = 2
            social_distancing_checkbox = 2
            bathroom_checkbox = 2
            wifi_checkbox = 2
            outlets_checkbox = 2
        else:
            masks_required_checkbox = 1 if "Masks required" in row[11] else 0
            staff_masks_checkbox = 1 if "Staff wears masks" in row[11] else 0
            plexiglass_checkbox = 1 if "Plexiglass at cashier" in row[11] else 0
            line_outside_checkbox = 1 if "Line outside" in row[11] else 0
            capacity_checkbox = 1 if "Limited capacity" in row[11] else 0
            takeout_checkbox = 1 if "Takeout" in row[11] else 0
            dine_in_checkbox = 1 if "Dine-in" in row[11] else 0
            outdoor_seating_checkbox = 1 if "Outdoor seating" in row[11] else 0
            social_distancing_checkbox = 1 if "Social distancing enforced" in row[11] else 0
            bathroom_checkbox = 2
            wifi_checkbox = 2
            outlets_checkbox = 2

        # update values in models table
        if place_id != "Other":
            # we are guaranteed to have the place model stored already
            # and therefore do not need to create a try except block for this
            place_model = Place.objects.get(pk=place_id)
            place_model.agg_density += crowded
            place_model.agg_density_n += 1
            place_model.agg_social += social_distancing
            place_model.agg_social_n += 1
            place_model.agg_mask += mask_wearing
            place_model.agg_mask_n += 1
            place_model.save()

        UserReport.objects.create(user_id=None, place_id=place_model, geohash_id=None, from_google_form=True,
                                  created=timestamp, start=start, end=end, density_rating=crowded,
                                  social_distancing_rating=social_distancing,
                                  mask_rating=mask_wearing, covid_rating=covid_protocol,
                                  masks_required_checkbox=masks_required_checkbox,
                                  staff_masks_checkbox=staff_masks_checkbox, plexiglass_checkbox=plexiglass_checkbox,
                                  line_outside_checkbox=line_outside_checkbox,
                                  capacity_checkbox=capacity_checkbox, takeout_checkbox=takeout_checkbox,
                                  dine_in_checkbox=dine_in_checkbox,
                                  outdoor_seating_checkbox=outdoor_seating_checkbox,
                                  social_distancing_checkbox=social_distancing_checkbox,
                                  bathroom_checkbox=bathroom_checkbox, wifi_checkbox=wifi_checkbox,
                                  outlets_checkbox=outlets_checkbox, other_comments=other_comments)

        count += 1

    print(datetime.now().strftime("[%m/%d/%Y %H:%M:%S] ") + "Collected " + str(
        count) + " new user reports from Google Forms.")

    return count
