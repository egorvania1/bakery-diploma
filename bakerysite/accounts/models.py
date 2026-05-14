from django.db import models
#from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User

# Create your models here.
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
        null=False, blank=False
    )

    class Meta:
        unique_together = (
            "user",
            "phone",
        )

    def __str__(self):
        return str(self.phone)