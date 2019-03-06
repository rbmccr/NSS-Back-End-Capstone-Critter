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
        Includes password confirmation.
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
        # this line is used to prevent crispy from automatically applying a form tag (i.e. I can wrap multiple forms together and define my own form tag and submit button)
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


class EditProfileUserForm(forms.ModelForm):
    """
        This class allows a user to edit their first_name, last_name, and email from their profile page.
        The __init__ method has been modified in order to display crispy forms in a specific way.
    """

    # def clean_email(self):
    #     cleaned_data = super(EditProfileUserForm, self).clean()
    #     my_email = cleaned_data.get('email')
    #     my_current_instance_id = CustomUser.objects.get(email=my_email).id
    #     users = CustomUser.objects.all()

    #     for user in users:
    #         if my_email == user.email:
    #             user_email_owner_id = CustomUser.objects.get(email=user.email).id
    #             print("$$$$$$$$$$$$$$$ user email owner id", user_email_owner_id, my_current_instance_id)
    #             if my_current_instance_id == user_email_owner_id:
    #                 pass
    #             else:
    #                 raise forms.ValidationError('')

        # return cleaned_data['email']

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
                Column('email', css_class='form-group col-md-6 mb-0')
            ),
        )

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name',)


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


class EditProfileVolunteerForm(forms.ModelForm):

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