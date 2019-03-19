# HTTP
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template import RequestContext
# models
from app.models import Animal

def index(request):

    recently_adopted_animals = Animal.objects.filter(date_adopted__isnull=False).exclude(image='/media/placeholder.jpg').order_by('date_adopted')[0:3]

    context = {
        'recently_adopted_animals': recently_adopted_animals,
    }

    return render(request, 'app/index.html', context)