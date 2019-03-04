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


class AnimalForm(forms.ModelForm):

    class Meta:
        model = Animal
        fields = ("name","age","species","breed","color","sex","image","description","date_arrival","staff",)


class ApplicationForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea, label='',)

    class Meta:
        model = Application
        fields = ("text",)