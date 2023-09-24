from django.urls import path
from . import views

urlpatterns = [
    path('set_open_status', views.set_is_open_status, name="set_open_status"),
    path('update_station_profile',
         views.edit_station_profile, name="update_station_profile"),
    path('update_station_amenities',
         views.edit_station_amenities, name="update_station_amenities"),
    path('update_fuel_products',
         views.edit_fuel_products, name="update_fuel_products"),
    path('get_stations_in_my_location',
         views.get_all_stations_in_my_location, name="get_stations_in_my_location"),
]
