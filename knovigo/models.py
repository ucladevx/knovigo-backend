from django.db import models

WEEKDAYS = [
  (1, _("Monday")),
  (2, _("Tuesday")),
  (3, _("Wednesday")),
  (4, _("Thursday")),
  (5, _("Friday")),
  (6, _("Saturday")),
  (7, _("Sunday")),
]

class Place(models.Model):
    google_place_id = models.IntegerField(primary_key=True)
    name = models.CharField()
    address = models.CharField()
    types = models.ArrayField(models.CharField)
    coordinates = models.PointField()


    rating = models.IntegerField()
    rating_n = models.IntegerField()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    hours = models.ForeignKey(BusinessHours)
    #other business info

    popular_times = models.ForeignKey(PopularTimes) #figure out

    covid_updates = models.ArrayField(models.CharField)
    confirmed_staff_infected = models.IntegerField()

    agg_density = models.IntegerField()
    agg_density_n = models.IntegerField()
    agg_social = models.IntegerField()
    agg_social_n = models.IntegerField()
    agg_mask = models.IntegerField()
    agg_mask_n = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

# account for holidays?
class BusinessHours(models.Model):
    id = models.AutoField(primary_key=true)
    place_id = models.ForeignKey(Place)
    weekday = models.IntegerField(choices=WEEKDAYS)
    from_hour = models.TimeField()
    to_hour = models.TimeField()

class PopularTimes(models.Model):
    id = models.AutoField(primary_key=true)
    place_id = models.ForeignKey(Place)

class UserReport(models.Model):
    report_id = models.AutoField(primary_key=True)
    user_id = model.ForeignKey(User, null=True) #ensure that we can have no users assigned for now
    place_id = model.ForeignKey(Place) 
    density_rating = model.IntegerField()
    social_distancing_rating = model.IntegerField()
    mask_rating = model.IntegerField()
    notes = model.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#including as a placeholder for now
class User(models.Model):
    id = models.AutoField(primary_key=true)

class GeoHash(models.Model):
    id = models.IntegerField(primary_key=true)
    # add LA Public health data for this region
