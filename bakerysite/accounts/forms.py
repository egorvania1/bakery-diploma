from phonenumber_field.formfields import PhoneNumberField
from django import forms
from django.contrib.auth.models import User

class UserLoginForm(forms.Form):
    #phone_number = PhoneNumberField(region="RU")
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
