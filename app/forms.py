from django.contrib.auth.models import User
from django import forms
from app.models import *

import itertools
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

class UserForm(forms.ModelForm):
    """
        This class is used in registration to define first_name, last_name, email, and password.
        The __init__ method has been modified in order to display crispy forms in a specific way.
    """
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'John'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Doe'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'johndoe@example.com'}))
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('email', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('password', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
        )

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'first_name', 'last_name',)


class VolunteerForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('phone_number', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('street_address', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('city', css_class='form-group col-md-6 mb-0'),
                Column('state', css_class='form-group col-md-4 mb-0'),
                Column('zipcode', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
        )

    class Meta:
        model = Volunteer
        fields = ('phone_number', 'street_address', 'city', 'state', 'zipcode',)


class AnimalForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea,)

    class Meta:
        model = Animal
        fields = ('name','age','species','breed','color','sex','image','description','date_arrival','staff',)


class ApplicationForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea, label='',)

    class Meta:
        model = Application
        fields = ('text',)