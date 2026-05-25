from django.contrib import admin

from travel_app.models import GeneralPackages, Attraction, PackagesAttraction

admin.site.register(GeneralPackages)
admin.site.register(Attraction)
admin.site.register(PackagesAttraction)
