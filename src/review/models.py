from django.db import models
from accounts.models import GeneralUser
from filling_station.models import FillingStation

# Create your models here.


class Review(models.Model):
    """Model for station review"""

    user = models.ForeignKey(GeneralUser, on_delete=models.CASCADE)
    review = models.CharField()
    date_of_review = models.DateField(auto_now_add=True)
    station = models.ForeignKey(FillingStation, on_delete=models.CASCADE)

    def __str__(self):
        return self.station
