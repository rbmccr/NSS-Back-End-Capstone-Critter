# authentication
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
# HTTP
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.urls import reverse
# messages
from django.contrib import messages
# models
from app.models import CustomUser, Application
# forms
from app.forms import UserForm, VolunteerForm, EditProfileUserForm, EditProfileVolunteerForm

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
        # get user instance to provide to form class
        user = CustomUser.objects.get(pk=request.user.id)
        edit_user_form = EditProfileUserForm(data=request.POST, instance=user)
        edit_volunteer_form = EditProfileVolunteerForm(data=request.POST)

        # check data types in submission. Django also checks to ensure username (e-mail in this project) is unique.
        if edit_user_form.is_valid() and edit_volunteer_form.is_valid():
            # Get user instance and update the user's data
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.save()

            # volunteer = edit_volunteer_form.save(commit=False)
            # volunteer.user = user
            # volunteer.save()

            # return to user profile
            return HttpResponseRedirect(reverse('app:profile'))

        else:
            # re-populate form with submitted data. Include message
            context = {
                'edit_user_form': edit_user_form,
                'edit_volunteer_form': edit_volunteer_form
            }

            messages.error(request, "Update failed.")
            return render(request, 'app/edit_profile.html', context)

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