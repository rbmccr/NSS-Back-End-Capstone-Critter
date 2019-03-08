# authentication
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
# HTTP
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.urls import reverse
# models
from app.models import Application, Animal
# messages
from django.contrib import messages

@staff_member_required
def list_applications(request):
    """
        This function gets all unadopted animals that have pending adoption applications and provides the list_applications template with a list of animals and a dictionary that contains animal ID's  as keys and number of apps as values
    """

    if request.method == 'GET':

        unadopted_animals = Animal.objects.filter(date_adopted=None)
        num_pending_applications = dict()
        animals = list()

        for animal in unadopted_animals:
            applications = Application.objects.filter(animal=animal).filter(approved=None)
            if len(applications) == 0:
                num_pending_applications[animal.id] = 0
                animals.append(animal)
            else:
                num_pending_applications[animal.id] = len(applications)
                animals.append(animal)

        context = {
            'animals': animals,
            'num_pending_applications': num_pending_applications
        }

        return render(request, 'app/list_applications.html', context)

@staff_member_required
def list_specific_applications(request, id):
    """
        This view function loads all pending and rejected applications for a specific animal
    """

    if request.method == 'GET':

        # check that animal is in the database and it isn't adopted yet
        animal = Animal.objects.filter(pk=id, date_adopted=None)

        try:
            animal = animal[0] # if animal has been adopted or doesn't exist, admin is redirected back
            applications = Application.objects.filter(animal=animal).filter(approved=None).order_by('date_submitted')
            rejections = Application.objects.filter(animal=animal).filter(approved=False).order_by('date_submitted')

            context = {
                'animal': animal,
                'applications': applications,
                'num_applications': len(applications) if not None else 0,
                'rejections': rejections,
                'num_rejections': len(rejections) if not None else 0
            }
            return render(request, 'app/list_specific_applications.html', context)
        except IndexError:
            return HttpResponseRedirect(reverse('app:list_applications'))

@staff_member_required
def final_decision(request, animal_id, application_id):
    """
        This view function is responsible for determining that the selected animal is not yet adopted before rendering a confirmation of adoption template for the administrator.
    """

    # check that animal is in the database and it isn't adopted yet
    animal = Animal.objects.filter(pk=animal_id, date_adopted=None)
    application = Application.objects.filter(pk=application_id)

    try:
        animal = animal[0] # if animal has been adopted or doesn't exist, admin is redirected to adoption manager page
        application = application[0] # if application doesn't exist, admin is redirected to adoption manager page

        if request.method == 'GET':
            context = {
                'animal': animal,
                'application': application,
            }
            return render(request, 'app/final_decision.html', context)

    except IndexError:
        messages.error(request, "Either the animal you're looking for was adopted or doesn't exist, or the application you're looking for isn't there.")
        return HttpResponseRedirect(reverse('app:list_applications'))


@staff_member_required
def reject_application(request, animal_id, application_id):
    """
        This view function is responsible for determining that the selected animal is not yet adopted before rendering a rejection template for the administrator.
    """

    # check that animal is in the database and it isn't adopted yet
    animal = Animal.objects.filter(pk=animal_id, date_adopted=None)
    application = Application.objects.filter(pk=application_id)

    try:
        animal = animal[0] # if animal has been adopted or doesn't exist, admin is redirected to adoption manager page
        application = application[0] # if application doesn't exist, admin is redirected to adoption manager page

        if request.method == 'GET':
            context = {
                'animal': animal,
                'application': application,
            }
            return render(request, 'app/reject_application.html', context)

    except IndexError:
        messages.error(request, "Either the animal you're looking for was adopted or doesn't exist, or the application you're looking for isn't there.")
        return HttpResponseRedirect(reverse('app:list_applications'))