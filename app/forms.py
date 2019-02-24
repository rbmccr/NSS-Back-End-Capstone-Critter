from django.contrib.auth.models import User
from django import forms
from app.models import *

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("username", "email", "password", "first_name", "last_name",)


class VolunteerForm(forms.ModelForm):

    class Meta:
        model = Volunteer
        fields = ("phone_number", "street_address", "city", "state", "zipcode",)