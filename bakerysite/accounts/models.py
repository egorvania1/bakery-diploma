from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# from django.contrib.auth.models import User
# from .models import User


# Create your models here.
class User(AbstractUser):
    USER_TYPES = {
        "EMPLOYEE": "Сотрудник",
        "CUSTOMER": "Посетитель",
    }

    patronymic = models.CharField(max_length=100, verbose_name="Отчество")
    user_type = models.CharField(max_length=8, null=False, blank=False, choices=USER_TYPES)


class Employee(models.Model):
    ROLES = {
        "ADMIN": "Администратор",
        "CONFE": "Кондитер",
    }

    user = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE)
    role = models.CharField(max_length=30, choices=ROLES, null=False, blank=False, verbose_name="Роль")

    class Meta:
        unique_together = (
            "user",
            "role",
        )

    def __str__(self):
        return str(self.user)


class Customer(models.Model):
    user = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE)
    phone = PhoneNumberField(
        null=False, blank=False, region="RU", unique=True, verbose_name="Номер телефона"
    )

    def __str__(self):
        return str(self.phone)
