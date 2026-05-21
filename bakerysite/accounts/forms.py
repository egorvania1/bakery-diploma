from phonenumber_field.formfields import PhoneNumberField
from django import forms
#from django.contrib.auth.models import User
from .models import Customer, User

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150, label="Имя пользователя")
    password = forms.CharField(widget=forms.PasswordInput(), max_length=50, label="Пароль")

class UserRegisterForm(forms.ModelForm):
    password_conf=forms.CharField(widget=forms.PasswordInput(), label="Подтвердите пароль")
    password = forms.CharField(widget=forms.PasswordInput(), max_length=50, label="Пароль")
    first_name = forms.CharField(required=True, label="Ваше имя")

    class Meta:
        model=User
        fields=['first_name', 'username', 'password']

    def clean(self):
        cleaned_data = super(UserRegisterForm, self).clean()
        password = cleaned_data.get("password")
        password_conf = cleaned_data.get("password_conf")

        if password != password_conf:
            raise forms.ValidationError(
                "Пароли не совпадают"
            )
        
        return cleaned_data

class ProfileRegisterForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields=('phone',)

class UserEditForm(forms.ModelForm):
    patronymic = forms.CharField(required=False, label="Отчество")

    class Meta:
        model=User
        fields=['first_name', 'last_name', 'patronymic', 'username']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields=('phone',)

class PasswordEditForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(), max_length=50, label="Пароль", required=False)
    password_conf = forms.CharField(widget=forms.PasswordInput(), label="Подтвердите пароль", required=False)

    def clean(self):
        cleaned_data = super(PasswordEditForm, self).clean()
        password = cleaned_data.get("password")
        password_conf = cleaned_data.get("password_conf")

        if password != password_conf:
            raise forms.ValidationError(
                "Пароли не совпадают"
            )
        
        return cleaned_data