from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    thalassemia_unit = models.ForeignKey(
        "clients.ThalassemiaUnit",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
    )

    def __str__(self):
        return self.email or self.username
