from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
'''
class User(AbstractUser):
    phone_number = PhoneNumberField(
        null=False, blank=False, unique=True, related_name="profile"
    )
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []
    objects = UserManager()
'''

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=30)

    class Meta:
        unique_together = ('user', 'role',)
    
    def __str__(self):
        return str(self.user)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = PhoneNumberField(
        null=False, blank=False, unique=True, related_name="profile"
    )

    class Meta:
        unique_together = (
            "user",
            "phone",
        )

    def __str__(self):
        return self.phone


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=30)

    class Meta:
        unique_together = (
            "user",
            "role",
        )

    def __str__(self):
        return str(self.user)
