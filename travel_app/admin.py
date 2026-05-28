from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from travel_app.models import GeneralPackages, Attraction, PackagesAttraction, CustomPackages, Client, Message, Booking, \
    Payment
from travel_app.views import AttractionCreateView

admin.site.register(GeneralPackages)
admin.site.register(Attraction)
admin.site.register(PackagesAttraction)
admin.site.register(CustomPackages)
class ClientAdmin(UserAdmin):
    model = Client

    fieldsets = UserAdmin.fieldsets + (
        ("Extra Info", {"fields": ("phone",)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Extra Info", {"fields": ("phone",)}),
    )
admin.site.register(Client, ClientAdmin)
admin.site.register(Message)
admin.site.register(Booking)
admin.site.register(Payment)