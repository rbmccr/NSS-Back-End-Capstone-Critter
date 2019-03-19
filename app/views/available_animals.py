# authentication
from django.contrib.admin.views.decorators import staff_member_required
# HTTP
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.urls import reverse
# messages
from django.contrib import messages
# models
from app.models import Animal, Application, Species, Breed, Color, CustomUser
# forms
from app.forms import AnimalForm
# util functions
from app.utils import establish_query, check_for_unadopted_animal

def available_animals(request):
    """
        This view function retrieves all unadopted animals from the animal table and renders a grid-based template to display bootstrap cards.

        args: request
    """

    animals = Animal.objects.filter(date_adopted=None).order_by('arrival_date')
    context = {
        'animals': animals,
        'animal_species': None,
        'animal_age': None
    }
    return render(request, 'app/available_animals.html', context)

def available_animals_search(request):
    """
        This view function is responsible for handling the filters and search functionality on the available animals page.

        args: request
    """

    form = request.GET
    # check for animal button name in form.
    if 'cat' in form:
        # if the value isn't already 'cat', set it to 'cat'
        if form.get('animal_species') != 'cat':
            animal_species = 'cat'
        # if the value is already 'cat', set the species to None
        else:
            animal_species = None
    elif 'dog' in form:
        if form.get('animal_species') != 'dog':
            animal_species = 'dog'
        else:
            animal_species = None
    elif 'other' in form:
        if form.get('animal_species') != 'other':
            animal_species = 'other'
        else:
            animal_species = None
    # if none of these options are in form, check to see if form.get('animal_species') is 'cat', 'dog', or 'other'
    # if so, keep the value the same. If the value is None, then do nothing
    else:
        if form.get('animal_species') is not 'None':
            animal_species = form.get('animal_species')

    # check for animal age button click in form.
    if 'young' in form:
        if form.get('animal_age') != 'young':
            animal_age = 'young'
        else:
            animal_age = None
    elif 'adult' in form:
        if form.get('animal_age') != 'adult':
            animal_age = 'adult'
        else:
            animal_age = None
    elif 'senior' in form:
        if form.get('animal_age') != 'senior':
            animal_age = 'senior'
        else:
            animal_age = None
    else:
        if form.get('animal_age') is not 'None':
            animal_age = form.get('animal_age')

    # check for text in search box
    if form.get('name_query') is not None or '':
        search_text = request.GET['name_query']
    else:
        search_text = None

    # if all filters are empty / cleared then load the standard pets page, else load the search page
    if (animal_species == None or animal_species == 'None') and (animal_age == None or animal_age == '' or animal_age == 'None') and(search_text == None or search_text == ''):
        return HttpResponseRedirect(reverse('app:pets'))

    filter_results = establish_query(animal_species, animal_age, search_text)

    context = {
        'animals': filter_results,
        'animal_count': len(filter_results) if filter_results is not None else 0,
        'animal_species': animal_species,
        'animal_age': animal_age,
        'search_text': search_text
    }
    return render(request, 'app/available_animals.html', context)

def animal_detail(request, animal_id):
    """
        This view retrieves a single animal from the animal table, checks to ensure the animal is not adopted or id doesn't exist (control for manual user navigation to the url) and renders a detail template (otherwise redirects user with notification of animal status).

        args: request, animal_id
    """

    animal = check_for_unadopted_animal(animal_id)

    if animal is None:
        messages.error(request, 'The animal you\'re looking for has been adopted or does not exist.')
        return HttpResponseRedirect(reverse('app:pets'))

    context = {
        'animal': animal,
    }

    # Check to see if a logged in user has already applied to adopt this animal. Get the status of their application if they have.
    if request.user.is_authenticated:
        application = Application.objects.filter(user=request.user, animal=animal)

        if len(application) == 1:
            context['existing_application'] = True
            context['application'] = application[0]

    return render(request, 'app/animal_detail.html', context)

@staff_member_required
def animal_edit(request, animal_id):
    """
        This view retrieves a single animal from the animal table, checks to ensure the animal is not adopted or id doesn't exist (control for manual user navigation to the url) and renders a pre-populated animal form for an administrator.

        On POST: animal instance is updated in database

        args: request, animal_id
    """

    animal = check_for_unadopted_animal(animal_id)

    if animal is None:
        messages.error(request, 'The animal you\'re looking for has been adopted or does not exist.')
        return HttpResponseRedirect(reverse('app:pets'))

    if request.method == 'GET':
        animal_form = AnimalForm(instance=animal)
        context = {
            'animal': animal,
            'animal_form': animal_form,
            'editing': True
            }
        return render(request, 'app/animal_form.html', context)

    if request.method == 'POST':
        animal_form = AnimalForm(data=request.POST, files=request.FILES)

        if animal_form.is_valid():
            animal.name = request.POST['name']
            animal.age = request.POST['age']
            animal.sex = request.POST['sex']
            animal.description = request.POST['description']
            animal.breed = Breed.objects.get(pk=request.POST['breed'])
            animal.color = Color.objects.get(pk=request.POST['color'])
            animal.species = Species.objects.get(pk=request.POST['species'])
            animal.staff = CustomUser.objects.get(pk=request.POST['staff'])
            animal.arrival_date = request.POST['arrival_date']
            if 'image' in request.FILES:
                animal.image.delete()
                animal.image = request.FILES['image']
            animal.save()

            messages.success(request, f'{animal.name} was updated successfully.')
            return HttpResponseRedirect(reverse('app:animal_detail', args=(animal_id,)))

        else:
            context = {
                'animal': animal,
                'animal_form': animal_form,
                'editing': True
            }
            messages.error(request, 'There was a problem with the edit. The request failed.')
            return render(request, 'app/animal_form.html', context)