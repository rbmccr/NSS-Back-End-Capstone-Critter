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

def determine_thumbnail(list_or_queryset):
    """
        This function is used with list_volunteering and volunteering_details to determine the proper thumbnail (a static file path) for each volunteering activity. Requires an iterable arg (list, queryset, etc.)

        Returns: dictionary in this format --> {'activity.id': 'static file path url'}
    """

    thumbnails = dict()

    for activity in list_or_queryset:
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

    return thumbnails

def list_volunteering(request):
    """
        This view function loads a list of all --> upcoming <-- volunteering activities and provides a static file path to the template to render an appropirate thumbnail.
    """

    now = datetime.datetime.now()
    activities = Activity.objects.filter(date__gte=now).order_by('date')

    # identify which thumbnail to use and pass in dictionary to template
    thumbnails = determine_thumbnail(activities)

    if request.method == 'GET':
        context = {
            'activities': activities,
            'thumbnails': thumbnails,
        }
        return render(request, 'app/list_volunteering.html', context)

def volunteering_details(request, activity_id):
    """
        This view function renders the detail page for a specific volunteering event after checking to ensure the event exists and/or has not been deleted.
    """

    activity = Activity.objects.filter(pk=activity_id)

    # ensure activity exists or has not been deleted using activity[0]
    try:
        activity = activity[0]
        # identify which thumbnail to pass into template (function requires an iterable arg)
        activity_list = [activity]
        thumbnail = determine_thumbnail(activity_list)
        thumbnail_url = thumbnail[activity_id]

        context = {
            'activity': activity,
            'thumbnail_url': thumbnail_url,
        }

        return render(request, 'app/volunteering_details.html', context)

    except IndexError:
        messages.error(request, "This volunteering opportunity doesn't exist. If you think you've signed up for an event that has been cancelled, please call us.")
        return HttpResponseRedirect(reverse('app:list_volunteering'))

@staff_member_required
def add_volunteering(request):
    """
        This view function provides a form for an administrator to create a new volunteering activity. A successful post saves an instance to the Activity table.
    """

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

@staff_member_required
def edit_volunteering(request, activity_id):
    """
        This view function checks to ensure the desired volunteering event exists --> AND <-- is upcoming (otherwise it redirects user), then pre-populates a form for an administrator to edit the existing volunteering activity.
    """

    now = datetime.datetime.now()
    activity = Activity.objects.filter(pk=activity_id).filter(date__gte=now)

    try:
        activity = activity[0]

        activity_data = {
            'activity': activity.activity,
            'date': activity.date,
            'description': activity.description,
            'start_time': activity.start_time,
            'end_time': activity.end_time,
            'activity_type': activity.activity_type,
            'max_attendance': activity.max_attendance,
        }

        activity_form = ActivityForm(data=activity_data)

        if request.method == 'GET':
            context = {
                'activity': activity,
                'activity_form': activity_form,
            }
            return render(request, 'app/edit_volunteering.html', context)

        if request.method == 'POST':

            activity_form = ActivityForm(data=request.POST)

            if activity_form.is_valid():
                # assign staff member and save form
                activity.staff = request.user
                activity.activity = request.POST['activity']
                activity.date = request.POST['date']
                activity.description = request.POST['description']
                activity.start_time = request.POST['start_time']
                activity.end_time = request.POST['end_time']
                activity.activity_type = request.POST['activity_type']
                activity.max_attendance = request.POST['max_attendance']
                activity.save()

                messages.success(request, 'You successfully edited this volunteering activity.')
                return HttpResponseRedirect(reverse('app:volunteering_details', args=(activity_id,)))

            else:
                context = {
                    'activity_form': activity_form,
                }
                return render(request, 'app/add_volunteering.html', context)

    except IndexError:
        messages.error(request, 'The volunteering activity you\'re trying to edit does not exist or occurred in the past.')
        return HttpResponseRedirect(reverse('app:list_volunteering'))