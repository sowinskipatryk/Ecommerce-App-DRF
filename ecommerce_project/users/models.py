from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    is_client = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
