from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.urls import reverse
from django.contrib import messages
from app.models import Animal

def available_animals(request):

    if request.method == 'GET':
        animals = Animal.objects.filter(date_adopted=None).order_by('date_arrival')
        context = {
            'animals': animals
        }
        return render(request, 'app/available_animals.html', context)

def animal_detail(request, id):

    if request.method == 'GET':
        animal = Animal.objects.filter(pk=id, date_adopted=None)

        # A user who manually navigates to an adopted animal's detail view is redirected to the main pets page -- animal[0] won't exist
        try:
            animal = animal[0]
            context = {
                'animal': animal
            }
            return render(request, 'app/animal_detail.html', context)

        except IndexError:
            messages.success(request, 'The animal you\'re looking for has been adopted.')
            return HttpResponseRedirect(reverse('app:pets'))