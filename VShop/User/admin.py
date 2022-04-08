from django import forms
from django.contrib import admin
# from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import User

@admin.register(User)
class PersonAdmin(admin.ModelAdmin):
    pass
# class Users:
#     class Meta:
#         model = User
#         fields = ('email', 'username', 'phone_number', 'password')


# class UserCreationForm(forms.ModelForm):
#     """A form for creating new users. Includes all the required
#     fields, plus a repeated password."""
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
#
#     class Meta:
#         model = User
#         fields = ('email', 'username', 'phone_number')
#
#     def clean_password2(self):
#         # Check that the two password entries match
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise ValidationError("Passwords don't match")
#         return password2
#
#     def save(self, commit=True):
#         # Save the provided password in hashed format
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user
#
#
# class UserChangeForm(forms.ModelForm):
#     """A form for updating users. Includes all the fields on
#     the user, but replaces the password field with admin's
#     disabled password hash display field.
#     """
#     password = ReadOnlyPasswordHashField()
#
#     class Meta:
#         model = User
#         fields = ('email', 'password', 'username', 'phone_number', 'is_active', 'is_staff')
#

# class MyAdmin(UserAdmin):
#     # The forms to add and change user instances
#     # form = UserChangeForm
#     # add_form = UserCreationForm
#     model = User
#
#     # The fields to be used in displaying the User model.
#     # These override the definitions on the base UserAdmin
#     # that reference specific fields on auth.User.
#     list_display = ('email', 'password', 'username', 'phone_number', 'is_active', 'is_staff')
#     list_filter = ('is_staff',)
#     # fieldsets = (
#     #     (None, {'fields': ('email', 'password')}),
#     #     ('Personal info', {'fields': ('username', 'phone_number')}),
#     #     ('Permissions', {'fields': ('is_staff',)}),
#     # )
#     # # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
#     # # overrides get_fieldsets to use this attribute when creating a user.
#     # add_fieldsets = (
#     #     (None, {
#     #         'classes': ('wide',),
#     #         'fields': ('email', 'username', 'phone_number', 'password1', 'password2'),
#     #     }),
#     # )
#     search_fields = ('email',)
#     ordering = ('email',)
#     filter_horizontal = ()
#
#
# # # Now register the new UserAdmin...
# #
# # class MyAdmin(UserAdmin):
# #     list_display = ("username", "phone_number", "email", "password", "is_staff")
# #     list_filter = ("username", "phone_number", "email", "password", "is_staff")
# #     search_fields = ("username", "phone_number", "email", "password", "is_staff")
#
#
# admin.site.register(User, MyAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
# admin.site.unregister(Group)

# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from .models import User
#
#
# class MyAdmin(BaseUserAdmin):
#     list_display = ("username", "phone_number", "email", "password", "is_admin")
#     list_filter = ("username", "phone_number", "email", "password", "is_admin")
#     search_fields = ("username", "phone_number", "email", "password", "is_admin")
#
#
# admin.site.register(User, MyAdmin)


