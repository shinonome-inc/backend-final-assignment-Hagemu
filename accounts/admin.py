from django.contrib import admin

from accounts.models import CustomUser, FriendShip

admin.site.register(CustomUser)
admin.site.register(FriendShip)
