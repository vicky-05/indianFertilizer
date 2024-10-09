from django.db import models
from django.contrib.auth.models import AbstractUser#
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):
    mobile_no = models.BigIntegerField(default=1111111111, validators=[MinValueValidator(1111111111), MaxValueValidator(9999999999)])
    profile_img = models.ImageField(upload_to='customer_profile_images/', default='customer_profile_images/default_img.png')

    def __str__(self):
        return self.username