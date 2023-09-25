from django.contrib import admin
from .models import FillingStation, FavouriteStation


class AdminFilligStation(admin.ModelAdmin):
    """Customize display for filling station model"""

    list_display = ['name', 'is_verified',
                    'license_number', 'address', 'location']


# Register your models here.
admin.site.register(FillingStation, AdminFilligStation)
admin.site.register(FavouriteStation)
