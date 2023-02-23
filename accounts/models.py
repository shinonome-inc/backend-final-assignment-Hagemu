from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    email = models.EmailField(_("email address"))
    following = models.ManyToManyField(
        "self",
        related_name="follow_by",
        through="FriendShip",
        symmetrical=False,
    )


class FriendShip(models.Model):
    follower = models.ForeignKey(
        CustomUser,
        related_name="follower",
        on_delete=models.CASCADE,
    )
    followed = models.ForeignKey(
        CustomUser,
        related_name="followed",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["follower", "followed"],
                name="unique_friendship",
            )
        ]
