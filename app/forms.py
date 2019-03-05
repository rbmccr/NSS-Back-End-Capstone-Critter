from django.contrib.auth.models import User
from django import forms
from app.models import *

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'email',
            'password'
        )

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'first_name', 'last_name',)


class VolunteerForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('city', css_class='form-group col-md-6 mb-0'),
                Column('state', css_class='form-group col-md-4 mb-0'),
                Column('zipcode', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Register', css_class='btn btn-dark')
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