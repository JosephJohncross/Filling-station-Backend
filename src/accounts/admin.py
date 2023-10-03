from django.contrib import admin
from .models import GeneralUser, User


class UserAdmin(admin.ModelAdmin):
    """"""
    list_display = ('email', 'is_active', 'role')
    # list_display_links = ('user')


# Register your models here.
admin.site.register(GeneralUser)
admin.site.register(User, UserAdmin)
