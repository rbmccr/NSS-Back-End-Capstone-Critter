from django.contrib.auth.models import User
from django import forms
from app.models import *

import itertools
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column

class UserForm(forms.ModelForm):
    """
        This class is used in registration to define first_name, last_name, email, and password.
        The __init__ method has been modified in order to display crispy forms in a specific way.
    """
    password = forms.CharField(widget=forms.PasswordInput(), label='Password (at least 8 characters)')
    confirm_password=forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('')

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row mb-n2'
            ),
            Row(
                Column('email', css_class='form-group col-md-6 mb-0'),
                css_class='form-row mb-n2'
            ),
            Row(
                Column('password', css_class='form-group col-md-6 mb-0'),
                Column('confirm_password', css_class='form-group col-md-6 mb-0'),
                css_class='form-row mb-n2'
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
                css_class='form-row mb-n2'
            ),
            Row(
                Column('street_address', css_class='form-group col-md-12 mb-0'),
                css_class='form-row mb-n2'
            ),
            Row(
                Column('city', css_class='form-group col-md-6 mb-0'),
                Column('state', css_class='form-group col-md-4 mb-0'),
                Column('zipcode', css_class='form-group col-md-2 mb-0'),
                css_class='form-row mb-n2'
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