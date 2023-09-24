from django.db import models
from accounts.models import User
from datetime import date, datetime, time
from autoslug import AutoSlugField
from django.utils.text import slugify
from cloudinary.models import CloudinaryField

# import for geos
from django.contrib.gis.db import models as gismodels
from django.contrib.gis.geos import Point


class FillingStation(models.Model):
    """Model representing each filling station"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    license_number = models.CharField(blank=True, null=True)
    petrol_price = models.IntegerField(blank=True, null=True)
    kerosene_price = models.IntegerField(blank=True, null=True)
    diesel_price = models.IntegerField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    filling_station_slug = AutoSlugField(populate_from=None, unique=True)
    no_of_favorites = models.IntegerField(default=0, blank=True)
    no_of_reviews = models.IntegerField(default=0, blank=True, null=True)
    total_clicks = models.IntegerField(default=0, blank=True, null=True)
    name = models.CharField(blank=True, null=True)
    operation_time = models.CharField(blank=True, null=True)
    car_wash = models.IntegerField(default=0)
    pos = models.IntegerField(default=0)
    car_mechanic = models.IntegerField(default=0)
    mini_mart = models.IntegerField(default=0)
    station_img = CloudinaryField(blank=True, null=True)
    address = models.CharField(blank=True, null=True)
    phone = models.CharField(blank=True, null=True)
    station_time = models.CharField(blank=True, null=True)
    is_open = models.BooleanField(default=False, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    longitude = models.CharField(max_length=20, blank=True, null=True)
    latitude = models.CharField(max_length=20, blank=True, null=True)
    location = gismodels.PointField(blank=True, null=True, srid=4326)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.latitude and self.longitude:
            self.location = Point(float(self.longitude), float(self.latitude))
        if not self.filling_station_slug:
            slug_text = f"{self.name}-{self.latitude, self.longitude}"
            self.filling_station_slug = slugify(slug_text)
        return super(FillingStation, self).save(*args, **kwargs)

    def is_opened(self):
        today_date = date.today()
        today = today_date.isoweekday()

        current_opening_hours = OpeningHour.objects.filter(
            filling_station=self, day=today)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        is_open = None
        for i in current_opening_hours:
            start = str(datetime.strptime(i.from_hour, "%I:%M %p").time())
            end = str(datetime.strptime(i.to_hour, "%I:%M %p").time())

            if current_time > start and current_time < end:
                is_open = True
            else:
                is_open = False

        return is_open


DAYS = [
    (1, ("Monday")),
    (2, ("Tuesday")),
    (3, ("Wednesday")),
    (4, ("Thursday")),
    (5, ("Friday")),
    (6, ("Saturday")),
    (7, ("Sunday"))
]

HOUR_OF_DAY_24 = [(time(h, m).strftime('%I:%M %p'), time(
    h, m).strftime('%I:%M %p')) for h in range(0, 24) for m in (0, 30)]


class OpeningHour(models.Model):
    """Model for station operating time"""

    filling_station = models.ForeignKey(
        FillingStation, on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS)
    from_hour = models.CharField(
        choices=HOUR_OF_DAY_24, max_length=10, blank=True)
    to_hour = models.CharField(
        choices=HOUR_OF_DAY_24, max_length=10, blank=True)
    is_closed = models.BooleanField(default=False, blank=True)

    class Meta:
        ordering = ('day', '-from_hour')
        unique_together = ('filling_station', 'day', 'from_hour', 'to_hour')

    def __str__(self):
        return self.get_day_display()
