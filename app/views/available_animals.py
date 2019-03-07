# HTTP
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.urls import reverse
# messages
from django.contrib import messages
# models
from app.models import Animal, Application, Species
# django tools
from django.db.models import Q


def available_animals(request):
    """
        This view retrieves all unadopted animals from the animal table and renders a grid-based template to display bootstrap cards.
    """

    if request.method == 'GET':
        animals = Animal.objects.filter(date_adopted=None).order_by('date_arrival')
        context = {
            'animals': animals,
            'animal_species': None,
            # 'animal_age': None
        }
        return render(request, 'app/available_animals.html', context)

def available_animals_search(request):
    """
        This view function is responsible for handling the filters and search functionality on the available animals page.
    """

    if request.method == "POST":
        post = request.POST
        # check for animal button name in post.
        if 'cat' in post:
            # if the value isn't already 'cat', set it to 'cat'
            if post['animal_species'] != 'cat':
                animal_species = 'cat'
            # if the value is already 'cat', set the species to None
            else:
                animal_species = None
        elif 'dog' in post:
            if post['animal_species'] != 'dog':
                animal_species = 'dog'
            else:
                animal_species = None
        elif 'other' in post:
            if post['animal_species'] != 'other':
                animal_species = 'other'
            else:
                animal_species = None
        # if none of these options are in post, check to see if post['animal_species'] is 'cat', 'dog', or 'other'
        # if so, keep the value the same. If the value is None, then do nothing
        else:
            if post['animal_species'] is not 'None':
                animal_species = post['animal_species']

        # check for animal age button click in post.
        if 'young' in post:
            if post['animal_age'] != 'young':
                animal_age = 'young'
            else:
                animal_age = None
        elif 'adult' in post:
            if post['animal_age'] != 'adult':
                animal_age = 'adult'
            else:
                animal_age = None
        elif 'senior' in post:
            if post['animal_age'] != 'senior':
                animal_age = 'senior'
            else:
                animal_age = None
        # if none of these options are in post, check to see if post['animal_age'] is 'young', 'adult', or 'senior'
        # if so, keep the value the same. If the value is None, then do nothing
        else:
            if post['animal_age'] is not 'None':
                animal_age = post['animal_age']

        # TODO: establish weeks/months/years column in db for use with this query
        if animal_age == None or animal_age == 'None':
            animal_age_instance = None
        else:
            animal_age_instance = None
            # animal_age_instance = Species.objects.get(species=animal_age)

        # TODO: handle search by name
        # search_text = request.POST["search_text"]
        # if search_text is not "":
        #     results = Animal.objects.filter(name__contains=search_text).order_by('date_arrival')
        #     context = {
        #         "results": results,
        #         "length": len(results),
        #         "search_text": search_text,
        #         "no_results": True if len(results) is 0 else False
        #     }
        # else:
        #     context = {
        #         "no_results": True,
        #         "search_text": search_text
        #     }

        search_text = None

        def establish_query(animal_species, animal_age, search_text):
            # animal_species
            if animal_species is None or animal_species == 'None' or animal_species == '':
                animal_species_query = None
            elif animal_species == 'other':
                animal_species_query = None
                # animal_species_query = Q(species=Species.objects.filter(Q(species='cat'), Q(species='dog')))
            else:
                animal_species_query = Q(species=Species.objects.get(species=animal_species))

            # animal_age
            if animal_age is None or animal_age == 'None' or animal_age == '':
                animal_age_query = None
            elif animal_age == 'young':
                animal_age_query = Q(age__lte=10)
            else:
                animal_age_query = Q(age__gt=10)

            # search_text
            if search_text is None or search_text == 'None' or search_text == '':
                pass
            else:
                search_query = Q(name__contains=search_text)

            # query_parameters = [animal_species_query, animal_age_query, search_query]
            filter_results = Animal.objects.filter(animal_species_query if animal_species_query is not None else Q(pk__gt=0) and Q(date_adopted=None))
            return filter_results

        filter_results = establish_query(animal_species, animal_age, search_text)


        # if animal_species is not None, we need to filter the results - but there are MANY 'other' species
        # if animal_species is not None and (animal_species == 'cat' or animal_species == 'dog'):
        #     animal_species_instance = Species.objects.get(species=animal_species)
        #     filter_results = Animal.objects.filter(Q(species=animal_species_instance), Q(date_adopted=None))
        # elif animal_species == 'other':
        #     cat_instance = Species.objects.get(species='cat')
        #     dog_instance = Species.objects.get(species='dog')
        #     filter_results = Animal.objects.filter(~Q(species=cat_instance), ~Q(species=dog_instance), Q(date_adopted=None))
        # else:
        #     filter_results = None


        context = {
            'animals': filter_results,
            # 'animal_count': len(filter_results) if filter_results is not None else 0,
            'animal_species': animal_species,
            'animal_age': animal_age,
            'search_text': search_text
        }

        #  TODO: set it up so if user clears both filters and text in search that all results appear
        print("@@@@@@@@@@@@", "spec", type(animal_species), animal_species, "age", type(animal_age), animal_age, "txt", type(search_text))
        if (animal_species == None or animal_species == 'None') and (animal_age == None or animal_age == '' or animal_age == 'None') and (search_text == None or search_text == ''):
            return HttpResponseRedirect(reverse('app:pets'))
        else:
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