from phonenumber_field.formfields import PhoneNumberField
from django import forms
from django.contrib.auth.models import User

class UserLoginForm(forms.Form):
    #phone_number = PhoneNumberField(region="RU")
    #username = forms.CharField(max_length=50)
    #username = PhoneNumberField(region="RU")
    username = forms.RegexField(regex=r'^[+][7]\d{10}$',
                                     error_messages = {"invalid": "Номер телефона должен быть введён в следующем формате: '+79994443322'"})
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
