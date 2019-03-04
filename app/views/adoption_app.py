from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.urls import reverse
from app.models import Animal, Application
from app.forms import ApplicationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def adoption_app(request, id):
    """
        This view retrieves a single animal from the animal table, checks to ensure the animal is not adopted or the id doesn't exist (control for manual user navigation to the url) and renders an adoption application template (otherwise redirects user with notification of animal status).
    """

    if request.method == 'GET':
        animal = Animal.objects.filter(pk=id, date_adopted=None)

        # A user who manually navigates to an adopted animal's detail view is redirected to the main pets page -- animal[0] won't exist
        try:
            animal = animal[0]
            app_form = ApplicationForm()
            context = {
                'animal': animal,
                'app_form': app_form
            }
            return render(request, 'app/adoption_app.html', context)

        except IndexError:
            messages.success(request, 'The animal you\'re looking for has been adopted or does not exist.')
            return HttpResponseRedirect(reverse('app:pets'))