from phonenumber_field.formfields import PhoneNumberField

class UserLoginForm(forms.Form):
    phone_number = PhoneNumberField(region="RU")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
