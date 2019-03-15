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

    if request.method == 'GET':
        animal_form = AnimalForm()
        context = {'animal_form': animal_form}
        return render(request, 'app/animal_form.html', context)

    if request.method == 'POST':
        form = AnimalForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the animal's form data to the database.
            form.save()
            messages.success(request, 'New arrival saved successfully!')
            return HttpResponseRedirect(reverse("app:pets"))