from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class User(AbstractUser):
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []
    objects = UserManager()
