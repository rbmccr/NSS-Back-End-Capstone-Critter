# authentication
from django.contrib.admin.views.decorators import staff_member_required
# HTTP
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.urls import reverse
# models
from app.models import Animal
# forms
from app.forms import AnimalForm
# messages
from django.contrib import messages

@staff_member_required
def new_arrival(request):
    """
        This view function renders a form for an administrator to upload a new animal. On POST, a new animal instance is added to the database in the Animal table.

        args: request
    """


    if request.method == 'GET':
        animal_form = AnimalForm()
        context = {'animal_form': animal_form}
        return render(request, 'app/animal_form.html', context)

    if request.method == 'POST':
        animal = AnimalForm(request.POST, request.FILES)
        if animal.is_valid():
            # Save the animal's form data to the database.
            animal.save()
            messages.success(request, 'New arrival saved successfully!')
            return HttpResponseRedirect(reverse("app:pets"))
        else:
            context = {'animal_form': animal_form}
            return render(request, 'app/animal_form.html', context)
            # TODO: check else logic for errors