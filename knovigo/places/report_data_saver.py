from django.http import HttpResponse
import json
from .scraper import WESTWOOD_LOCATIONS
from .models import Place, UserReport
from django.core.exceptions import FieldError
from datetime import datetime

# returns 0 on failure, 1 on success
def save_data_from_report(request):
    data = json.loads(request.body)
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S-0800")
    try:
        name = data["name"]
        place_id = WESTWOOD_LOCATIONS[name]

        # TODO: need to change these two based on frontend input
        start_stamp = data["start"]
        start = datetime.fromtimestamp(start_stamp).strftime("%Y-%m-%d %H:%M:%S-0800")
        end_stamp = data["end"]
        end = datetime.fromtimestamp(end_stamp).strftime("%Y-%m-%d %H:%M:%S-0800")
        density_rating = data["density"]
        social_distancing_rating = data["social_distancing"]
        mask_rating = data["mask"]
        covid_rating = data["covid"]

        masks_required_checkbox = data["masks_req"]
        staff_masks_checkbox = data["staff_masks_req"]
        plexiglass_checkbox = data["plexiglass_req"]
        line_outside_checkbox = data["line_req"]
        capacity_checkbox = data["capacity_limit_req"]
        takeout_checkbox = data["takeout_avlbl"]
        dine_in_checkbox = data["dinein_avlbl"]
        outdoor_seating_checkbox = data["outdoor_seats_avlbl"]
        social_distancing_checkbox = data["social_dist_req"]
        bathroom_checkbox = data["bathroom_avlbl"]
        wifi_checkbox = data["wifi_avlbl"]
        outlets_checkbox = data["outlets_avlbl"]

        coivd_notes = data["covid_notes"]
        other_comments = data["other_comments"]
    except KeyError:
        return 0, "Key not found"
    # update the corresponding place ID
    if place_id != "Other":
        # we are guaranteed to have the place model stored already
        # and therefore do not need to create a try except block for this
        place_model = Place.objects.get(pk=place_id)
        place_model.agg_density += density_rating
        place_model.agg_density_n += 1
        place_model.agg_social += social_distancing_rating
        place_model.agg_social_n += 1
        place_model.agg_mask += mask_rating
        place_model.agg_mask_n += 1
        place_model.save()
    else:
        return 0, "placeID not found"
    try:
        UserReport.objects.create(user_id=None, place_id=place_model, geohash_id=None, from_google_form=False,
                                  created=timestamp, start=start, end=end, density_rating=density_rating,
                                  social_distancing_rating=social_distancing_rating,
                                  mask_rating=mask_rating, covid_rating=covid_rating,
                                  masks_required_checkbox=masks_required_checkbox,
                                  staff_masks_checkbox=staff_masks_checkbox, plexiglass_checkbox=plexiglass_checkbox,
                                  line_outside_checkbox=line_outside_checkbox,
                                  capacity_checkbox=capacity_checkbox, takeout_checkbox=takeout_checkbox,
                                  dine_in_checkbox=dine_in_checkbox,
                                  outdoor_seating_checkbox=outdoor_seating_checkbox,
                                  social_distancing_checkbox=social_distancing_checkbox,
                                  bathroom_checkbox=bathroom_checkbox, wifi_checkbox=wifi_checkbox,
                                  outlets_checkbox=outlets_checkbox)
    except FieldError:
        return 0, "unable to create user report object"

    return 1, "success"
