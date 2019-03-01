from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template import RequestContext
from app.models import Animal

def available_pets(request):

    if request.method == 'GET':
        animals = Animal.objects.filter(date_adopted=None).order_by('date_arrival')
        context = {
            'animals': animals
        }
        return render(request, 'app/available_pets.html', context)