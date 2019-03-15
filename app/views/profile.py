# authentication
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
# HTTP
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.urls import reverse
# messages
from django.contrib import messages
# models
from app.models import CustomUser, Application, Volunteer
# forms
from app.forms import UserForm, VolunteerForm, EditProfileUserForm, EditProfileVolunteerForm, ChangePasswordForm
# local files
from .auth_views import login_user
# password validation
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

@login_required
def profile(request):
    """
        This view loads a user's personal profile, including their adoption applications submitted to the shelter.
    """

    if request.method == 'GET':
        user = request.user
        applications = Application.objects.filter(user=request.user)
        context = {
            'user': user,
            'applications': applications
        }
        return render(request, 'app/profile.html', context)

@login_required
def change_password(request):
    """
        This view provides a user with a form to update their password. A successful update will redirect the user back to their profile with a success message.
    """

    if request.method == 'GET':
        user = request.user
        new_password_form = ChangePasswordForm()
        context = {'new_password_form': new_password_form}
        return render(request, 'app/change_password.html', context)

    if request.method == 'POST':
        # get user instance used with form class instance (for validating unique fields) and volunteer instance
        user = CustomUser.objects.get(pk=request.user.id)
        old_password = request.POST['old_password']
        new_password_form = ChangePasswordForm(data=request.POST, instance=user)

        # validate password using installed validators in settings.py
        try:
            validate_password(request.POST['password']) == None
        except ValidationError:
            # return to form with form instance and message
            context = {'new_password_form': new_password_form}
            messages.error(request, "Password change failed. New password too simple.")
            return render(request, 'app/change_password.html', context)

        # verify requesting user's email and old_password match
        authenticated_user = authenticate(email=user.email, password=old_password)

        # check data types in submission.
        if new_password_form.is_valid() and authenticated_user is not None:
            # Note that user instance is used here for updating (not posting)
            # Hash the password and update the user object
            user.set_password(request.POST['password'])
            user.save()

            # re-authenticate with new password
            authenticated_user = authenticate(email=user.email, password=request.POST['password'])
            login(request=request, user=authenticated_user)

            # return to user profile with success message after logging user in with new credentials
            messages.success(request, "Password changed successfully!")
            return HttpResponseRedirect(request.POST.get('next', '/profile'))

        else:
            # return to form with form instance and message
            context = {'new_password_form': new_password_form}
            messages.error(request, "Password change failed. Old password incorrect or new passwords don't match")
            return render(request, 'app/change_password.html', context)

@login_required
def edit_profile(request):
    """
        This view function captures the current user's contact information and renders forms to edit the data.
        On POST, the user instance and volunteer instance are updated in the database.
    """

    if request.method == 'GET':
        user = request.user

        user_data = {
            'first_name':user.first_name,
            'last_name':user.last_name,
            'email': user.email
        }

        volunteer_data = {
            'phone_number':user.volunteer.phone_number,
            'street_address':user.volunteer.street_address,
            'city': user.volunteer.city,
            'state': user.volunteer.state,
            'zipcode': user.volunteer.zipcode
        }

        edit_user_form = EditProfileUserForm(initial=user_data)
        edit_volunteer_form = EditProfileVolunteerForm(initial=volunteer_data)

        context = {
            'user': user,
            'edit_user_form': edit_user_form,
            'edit_volunteer_form': edit_volunteer_form,
        }

        return render(request, 'app/edit_profile.html', context)

    if request.method == 'POST':
        # get user instance used with form class instance (for validating unique fields) and volunteer instance
        user = CustomUser.objects.get(pk=request.user.id)
        volunteer = Volunteer.objects.get(user=user)
        edit_user_form = EditProfileUserForm(data=request.POST, instance=user)
        edit_volunteer_form = EditProfileVolunteerForm(data=request.POST)

        # check data types in submission. Django also checks to ensure username (e-mail in this project) is unique.
        if edit_user_form.is_valid() and edit_volunteer_form.is_valid():
            # Note that user and volunteer instances are used here for updating (not posting)
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.save()

            volunteer.phone_number = request.POST['phone_number']
            volunteer.street_address = request.POST['street_address']
            volunteer.city = request.POST['city']
            volunteer.state = request.POST['state']
            volunteer.zipcode = request.POST['zipcode']
            volunteer.save()

            # return to user profile with success message
            messages.success(request, "Contact information updated successfully!")
            return HttpResponseRedirect(reverse('app:profile'))

        else:
            # re-populate form with submitted data. Include message
            context = {
                'edit_user_form': edit_user_form,
                'edit_volunteer_form': edit_volunteer_form
            }

            messages.error(request, "Update failed.")
            return render(request, 'app/edit_profile.html', context)