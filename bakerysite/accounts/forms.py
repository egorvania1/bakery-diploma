from phonenumber_field.formfields import PhoneNumberField
from django import forms
from django.contrib.auth.models import User
from .models import Customer

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class UserRegisterForm(forms.ModelForm):
    class Meta:
        model=User
        fields=('username', 'password',)

class ProfileRegisterForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields=('phone',)

