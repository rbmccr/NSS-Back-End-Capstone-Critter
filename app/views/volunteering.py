# authentication
from django.contrib.admin.views.decorators import staff_member_required
# HTTP
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.urls import reverse
# models
from app.models import Activity
# forms
from app.forms import ActivityForm
# messages
from django.contrib import messages
# tools
import datetime

def list_volunteering(request):

    now = datetime.datetime.now()
    activities = Activity.objects.filter(date__gte=now)

    # identify which thumbnail to use and pass in dictionary to template
    thumbnails = dict()

    for activity in activities:
        if activity.activity_type == 'cats':
            path = 'thumbnails/cat.png'
        elif activity.activity_type == 'dogs':
            path = 'thumbnails/dog.png'
        elif activity.activity_type == 'other':
            path = 'thumbnails/other.png'
        elif activity.activity_type == 'multi':
            path = 'thumbnails/multi.png'
        else:
            path = 'thumbnails/general.png'
        thumbnails[activity.id] = path

    if request.method == 'GET':
        context = {
            'activities': activities,
            'thumbnails': thumbnails,
        }
        return render(request, 'app/list_volunteering.html', context)

@staff_member_required
def add_volunteering(request):

    activity_form = ActivityForm()

    if request.method == 'GET':
        context = {
            'activity_form': activity_form,
        }
        return render(request, 'app/add_volunteering.html', context)

    if request.method == 'POST':

        activity_form = ActivityForm(data=request.POST)

        if activity_form.is_valid():
            # save form and assign staff member
            activity = activity_form.save(commit=False)
            activity.staff = request.user
            activity.save()

            return HttpResponseRedirect(reverse('app:list_volunteering'))

        else:
            context = {
                'activity_form': activity_form,
            }
            return render(request, 'app/add_volunteering.html', context)