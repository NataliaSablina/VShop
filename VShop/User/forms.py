from django import forms
from django.forms import TextInput

from .models import User


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.TextInput(attrs={'class': 'special', 'placeholder': "Enter Password",
                                                                               'onfocus':"this.className='focus'", 'onblur':"this.className='text'",
                                                                               }))
    password2 = forms.CharField(label="Repeat Password",
                                widget=forms.TextInput(attrs={'class': 'special', 'placeholder': "Enter Confirmation Of Password",
                                                                               'onfocus':"this.className='focus'", 'onblur':"this.className='text'",}))

    class Meta:
        model = User
        fields = ["username", "phone_number", "email"]
        widgets = {'username': TextInput(attrs={'class': 'special', 'placeholder': "Enter Name",
                                                                               'onfocus':"this.className='focus'", 'onblur':"this.className='text'",}),
                   'phone_number': TextInput(attrs={'class': 'special', 'placeholder': "Enter Phone Number",
                                                                               'onfocus':"this.className='focus'", 'onblur':"this.className='text'",}),
                   'email': TextInput(attrs={'class': 'special', 'placeholder': "Enter Email",
                                                                               'onfocus':"this.className='focus'", 'onblur':"this.className='text'",}),
                   'password': TextInput(attrs={'class': 'special', 'placeholder': "Enter Password",
                                                                               'onfocus':"this.className='focus'", 'onblur':"this.className='text'",}),
                   'password2': TextInput(attrs={'class': 'special', 'placeholder': "Enter Confirmation Of Password",
                                                                               'onfocus':"this.className='focus'", 'onblur':"this.className='text'",}),
                   }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd["password2"]


class UserAuthenticationForm(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class': 'special', 'placeholder': "Email",
                                                                               'onfocus':"this.className='focus'", 'onblur':"this.className='text'",}))
    password = forms.CharField(label="Password", widget=forms.TextInput(attrs={'class': 'special', 'placeholder': "Password",
                                                                               'onfocus':"this.className='focus'", 'onblur':"this.className='text'",}))


# class newUserRegistration(forms.Form):
# firstName = forms.CharField(widget=forms.TextInput(attrs={'type': 'text', 'id':'register-form-name', 'name':'register-form-name', 'value':"", 'class':'form-control'}))
# class Meta:
#     # specify model to be used
#     model = model_name
#     exclude = ()


