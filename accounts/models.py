from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = [
        ('senior', '어르신'),
        ('guardian', '보호자'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='senior'
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.username
