# authentication
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# HTTP
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.urls import reverse
# models
from app.models import Application, Animal

@login_required
def list_applications(request):

    if request.method == 'GET':

        unadopted_animals = Animal.objects.filter(date_adopted=None)
        num_pending_applications = dict()
        animals = list()

        for animal in unadopted_animals:
            applications = Application.objects.filter(animal=animal).filter(approved=None)
            if len(applications) == 0:
                pass
            else:
                num_pending_applications[animal.id] = len(applications)
                animals.append(animal)

        context = {
            'animals': animals,
            'num_pending_applications': num_pending_applications
        }

        return render(request, 'app/list_applications.html', context)