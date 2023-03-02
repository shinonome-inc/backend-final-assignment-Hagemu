from django.contrib import admin
from django.contrib.auth import get_user_model

from accounts.models import FriendShip

CustomUser = get_user_model()
admin.site.register(CustomUser)
admin.site.register(FriendShip)
