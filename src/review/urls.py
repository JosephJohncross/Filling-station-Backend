from django.urls import path
from . import views

urlpatterns = [
    path('create_review', views.create_a_review, name="create_review"),
    path('delete_review/<int:id>', views.delete_a_review, name="delete_review"),
    path('get_station_reviews/<int:id>', views.get_station_review,
         name='get_station_reviews')
]
