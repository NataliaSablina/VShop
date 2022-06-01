from django import forms
from django.contrib.auth.hashers import make_password
from django.forms import TextInput

from .models import User


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'special',
                                                              'placeholder': "Enter Confirmation Of Password",
                                                              'onfocus': "this.className='focus'",
                                                              'onblur': "this.className='text'", }))
    password2 = forms.CharField(label="Repeat Password",
                                widget=forms.PasswordInput(attrs={'class': 'special',
                                                                  'placeholder': "Enter Confirmation Of Password",
                                                                  'onfocus': "this.className='focus'",
                                                                  'onblur': "this.className='text'", }))

    class Meta:
        model = User
        fields = ["username", "phone_number", "email"]
        widgets = {'username': TextInput(attrs={'class': 'special',
                                                'placeholder': "Enter Name",
                                                'onfocus': "this.className='focus'",
                                                'onblur': "this.className='text'", }),

                   'phone_number': TextInput(attrs={'class': 'special',
                                                    'placeholder': "Enter Phone Number",
                                                    'onfocus': "this.className='focus'",
                                                    'onblur': "this.className='text'", }),

                   'email': TextInput(attrs={'class': 'special',
                                             'placeholder': "Enter Email",
                                             'onfocus': "this.className='focus'",
                                             'onblur': "this.className='text'", }),

                   'password': forms.PasswordInput(attrs={'class': 'special',
                                                'placeholder': "Enter Password",
                                                'onfocus': "this.className='focus'",
                                                'onblur': "this.className='text'", }),
                   'password2': forms.PasswordInput(attrs={'class': 'special',
                                                 'placeholder': "Enter Confirmation Of Password",
                                                 'onfocus': "this.className='focus'",
                                                 'onblur': "this.className='text'", }),
                   }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd["password2"]


class UserAuthenticationForm(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class': 'special',
                                                                          'placeholder': "Email",
                                                                          'onfocus': "this.className='focus'",
                                                                          'onblur': "this.className='text'", }))

    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'special',
                                                                               'placeholder': "Password",
                                                                               'onfocus': "this.className='focus'",
                                                                               'onblur': "this.className='text'", }))


class ChangeUserInformation(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'phone_number', 'email']
        widgets = {'username': TextInput(attrs={'class': 'user_change_special',
                                                'placeholder': "Enter Name",
                                                'onfocus': "this.className='user_change_focus'",
                                                'onblur': "this.className='user_change_text'", }),
                   'phone_number': TextInput(attrs={'class': 'user_change_special',
                                                    'placeholder': "Enter Phone Number",
                                                    'onfocus': "this.className='user_change_focus'",
                                                    'onblur': "this.className='user_change_text'", }),
                   'email': TextInput(attrs={'class': 'user_change_special',
                                             'placeholder': "Enter Email",
                                             'onfocus': "this.className='user_change_focus'",
                                             'onblur': "this.className='user_change_text'", })}


class ChangeUserPassword(forms.Form):
    old_password = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'class': 'user_change_special',
                                                                                 'placeholder': "Password",
                                                                                 'onfocus': "this.className"
                                                                                            "='user_change_focus'",
                                                                                 'onblur': "this.className"
                                                                                           "='user_change_text'", }))
    new_password = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'class': 'user_change_special',
                                                                                 'placeholder': "New Password",
                                                                                 'onfocus': "this.className"
                                                                                            "='user_change_focus'",
                                                                                 'onblur': "this.className"
                                                                                           "='user_change_text'", }))
    new_password2 = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'class': 'user_change_special',
                                                                                  'placeholder': "Confirm New Password",
                                                                                  'onfocus': "this.className"
                                                                                             "='user_change_focus'",
                                                                                  'onblur': "this.className"
                                                                                            "='user_change_text'", }))

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['new_password'] != cd['new_password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd["password2"]


class DeactivateAccount(forms.Form):
    password = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'class': 'user_change_special',
                                                                             'placeholder': "Password",
                                                                             'onfocus': "this.className"
                                                                                        "='user_change_focus'",
                                                                             'onblur': "this.className"
                                                                                       "='user_change_text'", }))


class ContactForm(forms.Form):
    to_email = forms.EmailField(label='Email', required=True, widget=forms.TextInput(attrs={'class': 'user_change_special',
                                                                             'placeholder': "Email",
                                                                             'onfocus': "this.className"
                                                                                        "='user_change_focus'",
                                                                             'onblur': "this.className"
                                                                                       "='user_change_text'", }))
    # # from_email = forms.EmailField(label='Email', required=True)
    # subject = forms.CharField(label='Тема', required=True)
    # message = forms.CharField(label='Сообщение', widget=forms.Textarea, required=True)


class ActivateAccountForm(forms.Form):
    email = forms.EmailField(label='Your Email', required=True, widget=forms.TextInput(attrs={'class': 'user_change_special',
                                                                             'placeholder': "Enter Email You Want Activate",
                                                                             'onfocus': "this.className"
                                                                                        "='user_change_focus'",
                                                                             'onblur': "this.className"
                                                                                       "='user_change_text'", }))
    subject = forms.CharField(label='Тема', required=True, widget=forms.TextInput(attrs={'class': 'user_change_special',
                                                                             'placeholder': "Enter Theme",
                                                                             'onfocus': "this.className"
                                                                                        "='user_change_focus'",
                                                                             'onblur': "this.className"
                                                                                       "='user_change_text'", }))
    message = forms.CharField(label='Сообщение', required=True, widget=forms.TextInput(attrs={'class': 'user_change_special',
                                                                             'placeholder': "Enter Message",
                                                                             'onfocus': "this.className"
                                                                                        "='user_change_focus'",
                                                                             'onblur': "this.className"
                                                                                       "='user_change_text'", }))


class HelpClientForm(forms.Form):
    name = forms.CharField(label='Full Name', required=True, widget=forms.TextInput(attrs={'class': 'user_change_special',
                                                                             'placeholder': "Enter Full Name",
                                                                             'onfocus': "this.className"
                                                                                        "='user_change_focus'",
                                                                             'onblur': "this.className"
                                                                                       "='user_change_text'", }))
    email = forms.EmailField(label='Email', required=True, widget=forms.TextInput(attrs={'class': 'user_change_special',
                                                                             'placeholder': "Enter Email",
                                                                             'onfocus': "this.className"
                                                                                        "='user_change_focus'",
                                                                             'onblur': "this.className"
                                                                                       "='user_change_text'", }))
    message = forms.CharField(label='How can we improve', required=True, widget=forms.TextInput(attrs={'class': 'user_change_special',
                                                                             'placeholder': "can we improve?",
                                                                             'onfocus': "this.className"
                                                                                        "='user_change_focus'",
                                                                             'onblur': "this.className"
                                                                                       "='user_change_text'", }))


