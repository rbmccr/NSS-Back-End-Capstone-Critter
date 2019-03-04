from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.urls import reverse
from app.models import Animal, Application
from app.forms import ApplicationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime

@login_required
def adoption_app(request, id):
    """
        This view performs one of two actions:
        1. On GET: Retrieves a single animal from the animal table, checks to ensure the animal is not adopted or the id doesn't exist (control for manual user navigation to the url) and renders an adoption application template (otherwise redirects user with notification of animal status).
        2. On POST: Saves an application for the specific animal to the database
    """

    if request.method == 'GET':
        animal = Animal.objects.filter(pk=id, date_adopted=None)

        # A user who manually navigates to an adopted animal's detail view is redirected to the main pets page -- animal[0] won't exist
        try:
            animal = animal[0]
            # TODO: check status of a user's app for this animal. if one exixts, look at app status and provide appropriate context to modify look of page
            app_form = ApplicationForm()
            context = {
                'animal': animal,
                'app_form': app_form
            }
            return render(request, 'app/adoption_app.html', context)

        except IndexError:
            messages.success(request, 'The animal you\'re looking for has been adopted or does not exist.')
            return HttpResponseRedirect(reverse('app:pets'))

    if request.method == 'POST':

        # first check to see if the animal has not been adopted with animal[0] (in case the user lingers on the page and an application is approved in the meantime)
        animal = Animal.objects.filter(pk=id, date_adopted=None)

        try:
            animal = animal[0] # if no match, move to except

            app_form = ApplicationForm(data = request.POST)

            if app_form.is_valid():
                new_app = Application(
                    user = request.user, # set submitter id as current user
                    text = request.POST['text'],
                    date_submitted = datetime.datetime.now(), # set date AND time of submission
                    animal = animal, # set animal id as the animal the user applied to adopt
                )
                new_app.save()

                messages.success(request, 'Thanks for applying to adopt! You can monitor the status of your application(s) here!')
                # TODO: reverse to my applications page of website
                return HttpResponseRedirect(reverse('app:pets'))

        except IndexError:
            messages.success(request, 'This animal has been adopted! There are plenty of forever friends left, though!')
            return HttpResponseRedirect(reverse('app:pets'))