# authentication
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# HTTP
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.urls import reverse
# models
from app.models import Animal, Application
# forms
from app.forms import ApplicationForm
# tools
import datetime
from app.utils import check_for_unadopted_animal

@login_required
def adoption_app(request, animal_id):
    """
        This view performs one of two actions:
        1. On GET: Retrieves a single animal from the animal table, checks to ensure the animal is not adopted or the id doesn't exist (control for manual user navigation to the url) and renders an adoption application template (otherwise redirects user with notification of animal status).
        2. On POST: Saves a user's application for a specific animal to the database

        args: request, animal_id
    """

    animal = check_for_unadopted_animal(animal_id)

    if request.method == 'GET':

        if animal is None:
            messages.error(request, 'The animal you\'re looking for has been adopted or does not exist.')
            return HttpResponseRedirect(reverse('app:pets'))

        # perform a secondary check to ensure that a user hasn't navigated around controls that prevent more than one application per user for a given animal (i.e. logged out view of animal detail -> click apply to adopt -> sign in). Another check is performed in the animal_detail view for a user navigating the site while already logged in.
        application = Application.objects.filter(user=request.user, animal=animal)

        if len(application) == 1:
            messages.error(request, 'Only one application can be submitted per animal.')
            return HttpResponseRedirect(reverse('app:animal_detail', args=(animal_id,)))
        else:
            app_form = ApplicationForm()
            context = {
                'animal': animal,
                'app_form': app_form,
            }
            return render(request, 'app/adoption_app.html', context)

    if request.method == 'POST':

        if animal is None:
            messages.error(request, 'This animal has been adopted! There are plenty of forever friends left, though!')
            return HttpResponseRedirect(reverse('app:pets'))

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
            return HttpResponseRedirect(reverse('app:profile'))