# HTTP
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.urls import reverse
# messages
from django.contrib import messages
# models
from app.models import Animal, Application, Species
# tools
from django.db.models import Q
import datetime
from dateutil.relativedelta import relativedelta

def available_animals(request):
    """
        This view retrieves all unadopted animals from the animal table and renders a grid-based template to display bootstrap cards.
    """

    if request.method == 'GET':
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
    """

    if request.method == "GET":
        post = request.GET
        # check for animal button name in post.
        if 'cat' in post:
            # if the value isn't already 'cat', set it to 'cat'
            if post.get('animal_species') != 'cat':
                animal_species = 'cat'
            # if the value is already 'cat', set the species to None
            else:
                animal_species = None
        elif 'dog' in post:
            if post.get('animal_species') != 'dog':
                animal_species = 'dog'
            else:
                animal_species = None
        elif 'other' in post:
            if post.get('animal_species') != 'other':
                animal_species = 'other'
            else:
                animal_species = None
        # if none of these options are in post, check to see if post.get('animal_species') is 'cat', 'dog', or 'other'
        # if so, keep the value the same. If the value is None, then do nothing
        else:
            if post.get('animal_species') is not 'None':
                animal_species = post.get('animal_species')

        # check for animal age button click in post.
        if 'young' in post:
            if post.get('animal_age') != 'young':
                animal_age = 'young'
            else:
                animal_age = None
        elif 'adult' in post:
            if post.get('animal_age') != 'adult':
                animal_age = 'adult'
            else:
                animal_age = None
        elif 'senior' in post:
            if post.get('animal_age') != 'senior':
                animal_age = 'senior'
            else:
                animal_age = None
        else:
            if post.get('animal_age') is not 'None':
                animal_age = post.get('animal_age')

        # check for text in search box
        if post.get('name_query') is not None or '':
            search_text = request.GET['name_query']
        else:
            search_text = None

        # if all filters are empty / cleared then load the standard pets page, else load the search page
        if (animal_species == None or animal_species == 'None') and (animal_age == None or animal_age == '' or animal_age == 'None') and (search_text == None or search_text == ''):
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

def animal_detail(request, id):
    """
        This view retrieves a single animal from the animal table, checks to ensure the animal is not adopted or id doesn't exist (control for manual user navigation to the url) and renders a detail template (otherwise redirects user with notification of animal status).
    """

    if request.method == 'GET':
        animal = Animal.objects.filter(pk=id, date_adopted=None)

        # A user who manually navigates to an adopted animal's detail view is redirected to the main pets page -- animal[0] won't exist
        try:
            animal = animal[0]
            context = {'animal': animal}

            # Check to see if a logged in user has already applied to adopt this animal. Get the status of their application if they have.
            if request.user.is_authenticated:
                application = Application.objects.filter(user=request.user, animal=animal)

                if len(application) == 1:
                    context = {
                        'animal': animal,
                        'existing_application': True,
                        'application': application[0]
                    }

            return render(request, 'app/animal_detail.html', context)

        except IndexError:
            messages.success(request, 'The animal you\'re looking for has been adopted or does not exist.')
            return HttpResponseRedirect(reverse('app:pets'))

# Helper functions ------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------

def establish_query(animal_species, animal_age, search_text):
    """
        This function accepts three filter arguments (strings), constructs a query based on conditional logic, and completes the query.

        args: animal_species, animal_age, search_text

        returns: complete queryset matching filters
    """

    # special query variables used with 'other' query
    cat_Q = None
    dog_Q = None

    # animal_species
    if animal_species is None or animal_species == 'None' or animal_species == '':
        species_Q = None
    elif animal_species == 'other':
        species_Q = None
        # need individual instances of cat and dog to provide main query below
        cat_Q = ~Q(species=Species.objects.get(species='cat'))
        dog_Q = ~Q(species=Species.objects.get(species='dog'))
    else:
        species_Q = Q(species=Species.objects.get(species=animal_species))

    # animal_age
    two_yrs_ago = datetime.datetime.now() - relativedelta(years=2)
    eight_yrs_ago = datetime.datetime.now() - relativedelta(years=8)

    if animal_age is None or animal_age == 'None' or animal_age == '':
        age_Q = None
    elif animal_age == 'young':
        age_Q = Q(age__gte=two_yrs_ago)
    elif animal_age == 'adult':
        age_Q = Q(age__gt=eight_yrs_ago, age__lt=two_yrs_ago)
    else:
        two_yrs_ago = datetime.datetime.now() - relativedelta(years=2)
        age_Q = Q(age__lte=eight_yrs_ago)

    # search_text
    if search_text is None or search_text == 'None' or search_text == '':
        search_Q = None
    else:
        search_Q = Q(name__contains=search_text)

    # get all with primary key > 0 (used in filter_results to get everything for that filter if the condition is none)
    _ = Q(pk__gt=0)
    # get only unadopted animals
    unadopted = Q(date_adopted=None)

    # filter(species).filter(ignore cat and dog species if 'other' selected).filter(age).filter(name).filter(unadopted animals)
    filter_results = Animal.objects.filter(species_Q if species_Q is not None else _).filter(cat_Q if cat_Q is not None else _).filter(dog_Q if dog_Q is not None else _).filter(age_Q if age_Q is not None else _).filter(search_Q if search_Q is not None else _).filter(unadopted)

    return filter_results