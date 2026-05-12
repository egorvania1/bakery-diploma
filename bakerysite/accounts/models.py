from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    full_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    # is_translator = models.BooleanField(default=False)
    objects = CustomUserManager()
    USERNAME_FIELD = 'phone_number'
    #REQUIRED_FIELDS = ['email', 'full_name']

    def __str__(self):
        return self.phone_number

    @staticmethod
    def has_perm(perm, obj=None, **kwargs):
        return True

    @staticmethod
    def has_module_perms(app_label, **kwargs):
        return True

    @property
    def is_staff(self):
        return self.is_admin