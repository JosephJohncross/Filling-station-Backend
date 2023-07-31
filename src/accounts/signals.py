from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import User, GeneralUser
from filling_station.models import FillingStation


@receiver(post_save, sender=User)
def post_save_create_user_profile_reciever(sender, instance, created, **kwargs):
    if created:
        if instance.role == 1:
            try:
                profile = GeneralUser.objects.get(user=instance)
                profile.save()
            except:
                # Create user profile if it doesn't exist
                GeneralUser.objects.create(user=instance)
        # elif instance.role == 2:
        #     try:
        #         profile = FillingStation.objects.get(user=instance)
        #         profile.save()
        #     except:
        #         # Create station user profile if it doesn't exist
        #         FillingStation.objects.create(user=instance)
        # else:
        #     print(type(instance))
