from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.models import User
from app.models import Application
from app.forms import UserForm, VolunteerForm

@login_required
def edit_profile(request):

    if request.method == 'GET':
        user = request.user
        applications = Application.objects.filter(user=request.user)
        context = {
            'edit_mode': True,
            'user': user,
            'applications': applications
        }
        return render(request, 'app/profile.html', context)

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