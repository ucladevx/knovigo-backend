from django.contrib import admin

from .models import Place, BusinessHours, PopularTimes, UserReport, User, GeoHash
admin.site.register(Place)
admin.site.register(BusinessHours)
admin.site.register(PopularTimes)
admin.site.register(UserReport)
admin.site.register(User)
admin.site.register(GeoHash)

# Register your models here.
