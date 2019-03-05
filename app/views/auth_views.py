from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template import RequestContext
from django.urls import reverse
from django.contrib import messages

from app.forms import UserForm, VolunteerForm

def register(request):
    '''Handles the creation of a new user for authentication
    Method arguments:
      request -- The full HTTP request object
    '''

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # Create a new user by invoking the `create_user` helper method
    # on Django's built-in User model
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        volunteer_form = VolunteerForm(data=request.POST)

        if user_form.is_valid() and volunteer_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            volunteer = volunteer_form.save(commit=False)
            volunteer.user = user
            volunteer.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        return login_user(request)

    elif request.method == 'GET':
        user_form = UserForm()
        volunteer_form = VolunteerForm()
        context = {'user_form': user_form, 'next': request.GET.get('next', '/'), 'volunteer_form': volunteer_form}
        return render(request, 'app/register.html', context)

# which would capture the next pass to registration form
# Upon submit grab the next value in the form on the post that will be passed down to login

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
            messages.error(request, "Login failed. Your email or password is incorrect.")

    return render(request, 'app/login.html', context)

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def logout_user(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')