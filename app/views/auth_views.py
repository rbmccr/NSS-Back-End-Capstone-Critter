# authentication
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
# HTTP
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.urls import reverse
# messages
from django.contrib import messages
# forms
from app.forms import UserForm, VolunteerForm
# password validation
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

def register(request):
    '''
        This function handles the submission of the registration form, including password and data type validation.
    '''

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        volunteer_form = VolunteerForm(data=request.POST)
        password = request.POST['password']

        # validate password using installed validators in settings.py
        try:
            validate_password(password) == None
        except ValidationError:
            # repopulate the form with submitted data. Include message
            context = {'user_form': user_form, 'next': request.GET.get('next', '/'), 'volunteer_form': volunteer_form}
            messages.error(request, "Registration failed. Password is too simple.")
            return render(request, 'app/register.html', context)

        # check data types in submission. Django also checks to ensure username (e-mail in this project) is unique
        if user_form.is_valid() and volunteer_form.is_valid():
            # Save the user's form data to the database
            user = user_form.save()

            # Hash the password and update the user object
            user.set_password(user.password)
            user.save()

            volunteer = volunteer_form.save(commit=False)
            volunteer.user = user
            volunteer.save()

            # login the registered user
            return login_user(request)
        else:
            # re-populate form with submitted data. Include message
            context = {'user_form': user_form, 'next': request.GET.get('next', '/'), 'volunteer_form': volunteer_form}
            messages.error(request, "Registration failed. If no error is displayed, passwords didn't match.")
            return render(request, 'app/register.html', context)

    elif request.method == 'GET':
        user_form = UserForm()
        volunteer_form = VolunteerForm()
        context = {'user_form': user_form, 'next': request.GET.get('next', '/'), 'volunteer_form': volunteer_form}
        return render(request, 'app/register.html', context)

def login_user(request):
    '''Handles the creation of a new user for authentication
    Method arguments:
      request -- The full HTTP request object
    '''

    # Obtain the context for the user's request.
    context = {'next': request.GET.get('next', '/')}

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Use the built-in authenticate method to verify
        email=request.POST['email']
        password=request.POST['password']
        authenticated_user = authenticate(email=email, password=password)

        # If authentication was successful, log the user in
        if authenticated_user is not None:
            login(request=request, user=authenticated_user)
            if request.POST.get('next') == '/':
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect(request.POST.get('next', '/'))

        else:
            # Bad login details were provided. So we can't log the user in.
            messages.error(request, "Login failed. Your e-mail or password is incorrect.")

    return render(request, 'app/login.html', context)

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def logout_user(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')