from django.db import models
from django.contrib.postgres.fields import ArrayField

# 0 indexing for popular times array
WEEKDAYS = [
    (0, ("Monday")),
    (1, ("Tuesday")),
    (2, ("Wednesday")),
    (3, ("Thursday")),
    (4, ("Friday")),
    (5, ("Saturday")),
    (6, ("Sunday")),
]

ALLOWED_TYPES = []  # add allowed store types

GEOHASH_LENGTH = 12


class Place(models.Model):
    # go through for what's allowed to be NULL JSADKLFJSDA:
    place_id = models.CharField(primary_key=True, max_length=60)

    # info taken from popular times
    name = models.CharField(max_length=60)
    address = models.CharField(max_length=60)
    types = ArrayField(models.CharField(max_length=60), null=True, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    rating = models.IntegerField()
    rating_n = models.IntegerField()
    # implicitly (using a 1-1 relationship) includes populartimes data (don't think we need the next line)
    # popular_times = models.ForeignKey('PopularTimes', on_delete=models.CASCADE, null=True, blank=True)

    # TODO: info taken from places api
    phone_number = models.CharField(max_length=60) # add validator
    # hours = models.ForeignKey('BusinessHours', on_delete=models.CASCADE, null=True, blank=True)
    website = models.CharField(max_length=60) #add validators
    # icon = models.CharField(max_length=60) # URL for icon - keep?
    price_level = models.IntegerField() # add restrictions! (0-4)
    # other business info

    # stuff from user reports
    # TODO: update this when a user report is submitted

    agg_density = models.IntegerField()
    agg_density_n = models.IntegerField()
    agg_social = models.IntegerField()
    agg_social_n = models.IntegerField()
    agg_mask = models.IntegerField()
    agg_mask_n = models.IntegerField()
    covid_updates = ArrayField(models.CharField(max_length=60), null=True, blank=True)  # todo

    confirmed_staff_infected = models.IntegerField()  # not sure where we're getting this from

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class PopularTimes(models.Model):
    place = models.OneToOneField(Place, on_delete=models.CASCADE, primary_key=True)

    monday = ArrayField(models.IntegerField(null=True, blank=True), null=True, blank=True)
    tuesday = ArrayField(models.IntegerField(null=True, blank=True), null=True, blank=True)
    wednesday = ArrayField(models.IntegerField(null=True, blank=True), null=True, blank=True)
    thursday = ArrayField(models.IntegerField(null=True, blank=True), null=True, blank=True)
    friday = ArrayField(models.IntegerField(null=True, blank=True), null=True, blank=True)
    saturday = ArrayField(models.IntegerField(null=True, blank=True), null=True, blank=True)
    sunday = ArrayField(models.IntegerField(null=True, blank=True), null=True, blank=True)


# account for holidays?
class BusinessHours(models.Model):
    place = models.OneToOneField(Place, on_delete=models.CASCADE, primary_key=True)
    monday_open = models.IntegerField(null=True, blank=True)
    monday_close = models.IntegerField(null=True, blank=True)
    tuesday_open = models.IntegerField(null=True, blank=True)
    tuesday_close = models.IntegerField(null=True, blank=True)
    wednesday_open = models.IntegerField(null=True, blank=True)
    wednesday_close = models.IntegerField(null=True, blank=True)
    thursday_open = models.IntegerField(null=True, blank=True)
    thursday_close = models.IntegerField(null=True, blank=True)
    friday_open = models.IntegerField(null=True, blank=True)
    friday_close = models.IntegerField(null=True, blank=True)
    saturday_open = models.IntegerField(null=True, blank=True)
    saturday_close = models.IntegerField(null=True, blank=True)
    sunday_open = models.IntegerField(null=True, blank=True)
    sunday_close = models.IntegerField(null=True, blank=True)


class UserReport(models.Model):
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


# including as a placeholder for now
class User(models.Model):
    id = models.AutoField(primary_key=True)


class GeoHash(models.Model):
    id = models.CharField(primary_key=True, max_length=GEOHASH_LENGTH)  # change to a constant
    name = models.CharField(max_length=60)
    # add LA Public health data for this region
