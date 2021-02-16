from django.http import HttpResponse
import json
from .scraper import WESTWOOD_LOCATIONS
from .models import Place, UserReport
"""
    report_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE,
                                null=True)  # ensure that we can have no users assigned for now

    # TODO: place/geohash should be connected to places api
    place_id = models.ForeignKey('Place', on_delete=models.CASCADE, null=True)
    geohash_id = models.ForeignKey('GeoHash', on_delete=models.CASCADE, null=True)
    from_google_form = models.BooleanField()  # differentiate between app vs google form reports

    created = models.DateTimeField()
    updated = models.DateTimeField(auto_now=True)

    start = models.DateTimeField()
    end = models.DateTimeField()

    density_rating = models.IntegerField()
    social_distancing_rating = models.IntegerField()
    mask_rating = models.IntegerField()
    covid_rating = models.IntegerField()

    # select all that apply options
    # integer - 0 = false, 1 = true, 2 = not specified
    masks_required_checkbox = models.IntegerField()
    staff_masks_checkbox = models.IntegerField()
    plexiglass_checkbox = models.IntegerField()
    line_outside_checkbox = models.IntegerField()
    capacity_checkbox = models.IntegerField()
    takeout_checkbox = models.IntegerField()
    dine_in_checkbox = models.IntegerField()
    outdoor_seating_checkbox = models.IntegerField()
    social_distancing_checkbox = models.IntegerField()
    bathroom_checkbox = models.IntegerField()
    wifi_checkbox = models.IntegerField()
    outlets_checkbox = models.IntegerField()

    covid_notes = models.TextField()
    other_comments = models.TextField()
"""
def save_data_from_report(request):

    data = json.loads(request.body)
    user_id = data["userid"]
    id = data["id"]
    print(user_id, id)
    return 0
    # name = data["name"]
    # place_id = WESTWOOD_LOCATIONS[name]
    #
    # # TODO: need to change these two based on frontend input
    # start = None
    # end = None
    # density_rating = data["density"]
    # social_distancing_rating = data["social_distancing"]
    # mask_rating = data["mask"]
    # covid_rating = data["covid"]
    #
    # masks_required_checkbox = data["masks_req"]
    # staff_masks_checkbox = data["staff_masks_req"]
    # plexiglass_checkbox = data["plexiglass_req"]
    # line_outside_checkbox = data["line_req"]
    # capacity_checkbox = data["capacity_limit_req"]
    # takeout_checkbox = data["takeout_avlbl"]
    # dine_in_checkbox = data["dinein_avlbl"]
    # outdoor_seating_checkbox = data["outdoor_seats_avlbl"]
    # social_distancing_checkbox = data["social_dist_req"]
    # bathroom_checkbox = data["bathroom_avlbl"]
    # wifi_checkbox = data["wifi_avlbl"]
    # outlets_checkbox = data["outlets_avlbl"]
    #
    # coivd_notes = data["covid_notes"]
    # other_comments = data["other_comments"]
    #
    # # update the corresponding place ID
    # if place_id != "Other":
    #     # we are guaranteed to have the place model stored already
    #     # and therefore do not need to create a try except block for this
    #     place_model = Place.objects.get(pk=place_id)
    #     place_model.agg_density += density_rating
    #     place_model.agg_density_n += 1
    #     place_model.agg_social += social_distancing_rating
    #     place_model.agg_social_n += 1
    #     place_model.agg_mask += mask_rating
    #     place_model.agg_mask_n += 1
    #     place_model.save()
    # else:
    #     return -1, "placeID not found"
    #
    # UserReport.objects.create(user_id=None, place_id=place_model, geohash_id=None, from_google_form=True,
    #                           created=timestamp, start=start, end=end, density_rating=density_rating,
    #                           social_distancing_rating=social_distancing_rating,
    #                           mask_rating=mask_rating, covid_rating=covid_rating,
    #                           masks_required_checkbox=masks_required_checkbox,
    #                           staff_masks_checkbox=staff_masks_checkbox, plexiglass_checkbox=plexiglass_checkbox,
    #                           line_outside_checkbox=line_outside_checkbox,
    #                           capacity_checkbox=capacity_checkbox, takeout_checkbox=takeout_checkbox,
    #                           dine_in_checkbox=dine_in_checkbox,
    #                           outdoor_seating_checkbox=outdoor_seating_checkbox,
    #                           social_distancing_checkbox=social_distancing_checkbox,
    #                           bathroom_checkbox=bathroom_checkbox, wifi_checkbox=wifi_checkbox,
    #                           outlets_checkbox=outlets_checkbox)
    #
    # return 0
