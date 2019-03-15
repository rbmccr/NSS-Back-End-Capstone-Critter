# models
from .models import Animal, Species
# tools
from django.db.models import Q
from dateutil.relativedelta import relativedelta
import datetime

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