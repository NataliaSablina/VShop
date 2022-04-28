from django import forms
from .models import User


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password")
    password2 = forms.CharField(label="repeat Password")

    class Meta:
        model = User
        fields = ["username", "phone_number", "email"]

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd["password2"]


class UserAuthenticationForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password")


