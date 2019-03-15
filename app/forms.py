from django.contrib.auth.models import User
from django import forms
# models
from app.models import *
# crispy
import itertools
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, ButtonHolder
# tools
import datetime

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

class ChangePasswordForm(forms.ModelForm):
    """
        This class allows a user to edit their first_name, last_name, and email from their profile page.
        The __init__ method has been modified in order to display crispy forms in a specific way.
    """

    old_password = forms.CharField(widget=forms.PasswordInput(), label='Old password')
    password = forms.CharField(widget=forms.PasswordInput(), label='Password (at least 8 characters)')
    confirm_password=forms.CharField(widget=forms.PasswordInput(),  label='Confirm new password')

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('old_password', css_class='form-group col-md-6 mb-0'),
                css_class='form-row mb-n2'
            ),
            Row(
                Column('password', css_class='form-group col-md-6 mb-0'),
                Column('confirm_password', css_class='form-group col-md-6 mb-0')
            ),
        )

    class Meta:
        model = CustomUser
        fields = ('password',)


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
    """
        This form class is used for new animal arrivals to the shelter. It includes most fields from the Animal model. Arrival date defaults to the current date.
    """

    name = forms.CharField(label='Name (16 characters or fewer)')
    description = forms.CharField(widget=forms.Textarea,)

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_tag = False
            # default arrival date to today
            self.fields['arrival_date'].initial = datetime.datetime.today()
            # get staff names instead of emails
            self.fields['staff'].label_from_instance = lambda obj: "%s" % obj.get_full_name()
            self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-4 mb-0'),
                Column('age', css_class='form-group col-md-4 mb-0'),
                Column('sex', css_class='form-group col-md-4 mb-0'),
                css_class='form-row mb-n2'
            ),
            Row(
                Column('species', css_class='form-group col-md-4 mb-0'),
                Column('breed', css_class='form-group col-md-4 mb-0'),
                Column('color', css_class='form-group col-md-4 mb-0'),
                css_class='form-row mb-n2'
            ),
            Row(
                Column('description', css_class='form-group col-md-12 mb-0'),
                css_class='form-row mb-n2'
            ),
            Row(
                Column('image', css_class='form-group col-md-4 mb-0'),
                Column('arrival_date', css_class='form-group col-md-4 mb-0'),
                Column('staff', css_class='form-group col-md-4 mb-0'),
                css_class='form-row mb-n2'
            ),
        )

    class Meta:
        model = Animal
        fields = ('name','age','species','breed','color','sex','image','description','arrival_date','staff',)
        widgets = {
            'arrival_date': forms.DateInput(attrs={"type": "date"}),
            'age': forms.DateInput(attrs={"type": "date"})
        }
        labels = {
            'age': 'Est. birthday'
        }


class ApplicationForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea, label='',)

    class Meta:
        model = Application
        fields = ('text',)


class RejectionForm(forms.ModelForm):
    reason = forms.CharField(widget=forms.Textarea(attrs={'rows':5}), label='')

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_tag = False
            self.fields['reason'].initial = 'Thank you for your interest in this animal. While we believe that there is another, more suitable applicant for this animal, we hope you will consider adopting another pet!'

    class Meta:
        model = Application
        fields = ('reason',)


class ActivityForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':10}))

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_tag = False
            self.helper.layout = Layout(
            Row(
                Column('activity', css_class='form-group col-md-6 mb-0'),
                Column('activity_type', css_class='form-group col-md-3 mb-0'),
                css_class='form-row mb-n2'
            ),
            Row(
                Column('description', css_class='form-group col-md-12 mb-0'),
                css_class='form-row mb-n2'
            ),
            Row(
                Column('date', css_class='form-group col-md-3 mb-0'),
                Column('start_time', css_class='form-group col-md-3 mb-0'),
                Column('end_time', css_class='form-group col-md-3 mb-0'),
                Column('max_attendance', css_class='form-group col-md-3 mb-0'),
                css_class='form-row mb-n2'
            ),
        )

    class Meta:
        model = Activity
        fields = ('activity','description','date','start_time','end_time','max_attendance','activity_type')
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "end_time": forms.TimeInput(attrs={"type": "time"})
        }