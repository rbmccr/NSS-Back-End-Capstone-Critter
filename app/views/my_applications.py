from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.urls import reverse
from django.contrib import messages
from app.models import Application
from django.contrib.auth.decorators import login_required

@login_required
def personal_applications(request):
    user = request.user
    applications = Application.objects.filter(user=user)
    context = {
        'applications': applications
    }
    return render(request, 'app/my_applications.html', context)