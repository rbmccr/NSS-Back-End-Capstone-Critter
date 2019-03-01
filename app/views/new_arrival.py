from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template import RequestContext
from django.urls import reverse
from app.models import Animal
from app.forms import AnimalForm
from django.contrib import messages

def new_arrival(request):

    if request.method == 'GET':
        animal_form = AnimalForm()
        context = {
            'animal_form': animal_form
        }
        return render(request, 'app/new_arrival.html', context)

    if request.method == 'POST':
        form = AnimalForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the animal's form data to the database.
            form.save()
            messages.success(request, 'Saved new arrival!')
            return HttpResponseRedirect(reverse("app:index"))