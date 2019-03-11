# authentication
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
# HTTP
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.urls import reverse
# models
from app.models import Application, Animal, CustomUser
# messages
from django.contrib import messages
# forms
from app.forms import RejectionForm

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

    # check that animal and application are in the database and animal isn't adopted yet
    animal = Animal.objects.filter(pk=animal_id, date_adopted=None)
    application = Application.objects.filter(pk=application_id)

    try:
        animal = animal[0] # if animal has been adopted or doesn't exist, admin is redirected to adoption manager page
        application = application[0] # if application doesn't exist, admin is redirected to adoption manager page

        rejection_form = RejectionForm()

        if request.method == 'GET':
            context = {
                'animal': animal,
                'application': application,
                'rejection_form': rejection_form
            }
            return render(request, 'app/reject_application.html', context)

        if request.method == 'POST':
            rejection_form = RejectionForm(data=request.POST)

            if rejection_form.is_valid():
                # capture rejection reason provided
                application.reason = request.POST['reason']
                # assign staff memeber who provided rejection to the application
                application.staff = request.user
                # apply rejection and save
                application.approved = False
                application.save()

                messages.success(request, f"You rejected the application submitted by {application.user.first_name} {application.user.last_name}")
                return HttpResponseRedirect(reverse('app:list_specific_applications', args=(animal_id,)))
            else:
                messages.error(request, "There was a problem with your rejection. Please try again.")
                return HttpResponseRedirect(reverse('app:list_specific_applications', args=(animal_id,)))

    except IndexError:
        messages.error(request, "Either the animal you're looking for was adopted or doesn't exist, or the application you're looking for isn't there.")
        return HttpResponseRedirect(reverse('app:list_applications'))

@staff_member_required
def revise_judgment(request, animal_id, application_id):
    """
        This view function is responsible for determining that the selected animal is not yet adopted before removing the False condition from Application.approved.
    """

    # check that animal and application are in the database and animal isn't adopted yet
    animal = Animal.objects.filter(pk=animal_id, date_adopted=None)
    application = Application.objects.filter(pk=application_id)

    try:
        animal = animal[0] # if animal has been adopted or doesn't exist, admin is redirected to adoption manager page
        application = application[0] # if application doesn't exist, admin is redirected to adoption manager page

        if request.method == 'GET':
            # get instance of application
            application = Application.objects.get(pk=application_id)
            # assign staff memeber who revised rejection to the application
            application.staff = request.user
            # apply revision (i.e. change 0 to null in database)
            application.approved = None
            application.save()
            messages.success(request, f"The application submitted by {application.user.first_name} {application.user.last_name} was marked for revision.")
            return HttpResponseRedirect(reverse('app:list_specific_applications', args=(animal_id,)))

    except IndexError:
        messages.error(request, "Either the animal you're looking for was adopted or doesn't exist, or the application you're looking for isn't there.")
        return HttpResponseRedirect(reverse('app:list_applications'))