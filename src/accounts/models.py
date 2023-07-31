from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
# from filling_station.models import FillingStation
from django.contrib.gis.db import models as gismodels
from django.contrib.gis.geos import Point


class UserManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, password=None):
        """"Create a new user profile"""

        if not email:
            raise ValueError("Users must have a staff ID to have an account")

        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        user.is_active = False

        return user

    def create_superuser(self, email, password):
        """Create and save a new superuser with given details"""

        user = self.create_user(email=email)

        user.set_password(password)
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superadmin = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""

    email = models.EmailField(max_length=100, unique=True)
    is_station_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    role = models.IntegerField(blank=True, null=True, default=0)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []

    def __str__(self):
        """Return string representation of user"""
        return self.email


class GeneralUser(models.Model):
    """Model for normal users"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    name = models.CharField(blank=True, null=True)
    phone = models.CharField(blank=True, null=True)
    avatar = models.CharField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.name
    # general_user = models.OneToOneField(
    #     User, on_delete=models.CASCADE, primary_key=True)
    # favorite=models.ForeignKey(FillingStation, on_delete=models.CASCADE)
