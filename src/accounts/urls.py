from django.urls import path
from . import views

urlpatterns = [
    path('create_user', views.create_general_user, name="create_user"),
    path('update_user', views.update_general_user, name="update_user"),
    path('delete_user', views.delete_general_user, name="delete_user"),
    path('get_users', views.get_users, name="get_user"),

    # Station
    path('create_station', views.create_station, name="create_station"),
    path('update_station', views.update_station, name="update_station"),
    path('delete_station', views.delete_station, name="delete_station"),
    path('get_stations', views.get_stations, name="get_stations"),
    path('get_station/<slug:slug>',
         views.get_stations_by_slug, name="get_stations_by_slug"),
    path('get_statistics', views.get_admin_statistics, name="get_statistics"),
    path('get_station_dashboard_profile/<int:user_id>', views.get_station_dashboard_profile,
         name="get_station_dashboard_profile"),
]
