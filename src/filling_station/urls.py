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
    path('give_rating', views.rate_station, name="give_rating"),
    path('add_station_to_favorite', views.add_station_to_favorite,
         name="add_station_to_favorite"),
    path('get_favourite_station/<int:user_id>', views.get_favourite_station,
         name='get_favourite_station'),
    path('remove_station_from_favourite/<int:station>/<int:user>', views.remove_favourite,
         name='remove_station_from_favourite'),
    path('verify_station/<int:id>', views.verify_station, name='verify_station'),
    path('update_station_img', views.update_station_img, name='update_station_img'),
    path('search_for_station',
         views.user_station_search, name="search_for_station")
]
