# authentication
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
# HTTP
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.urls import reverse
# models
from app.models import Activity, ActivityVolunteer
# forms
from app.forms import ActivityForm
# messages
from django.contrib import messages
# tools
import datetime
from app.utils import determine_thumbnail, check_if_user_is_signed_up

def list_volunteering(request):
    """
        This view function loads a list of all --> upcoming <-- volunteering activities (including cancelled activites) and provides a static file path to the template to render an appropirate thumbnail.
    """

    now = datetime.datetime.now()
    activities = Activity.objects.filter(date__gte=now).order_by('date')

    # identify which thumbnail to use and pass in dictionary to template
    thumbnails = determine_thumbnail(activities)

    # use single loop to get day of week for each event and determine which events user is signed up for
    signed_up = list()
    day_of_week = dict()
    for activity in activities:
        # get day of week for use with date listing
        day = datetime.datetime.strptime(str(activity.date), '%Y-%m-%d').strftime('%a')
        day_of_week[activity.id] = day
        # identify which events the current user (if there is one) is signed up for
        if request.user.is_authenticated:
            if check_if_user_is_signed_up(request.user, activity) == True:
                signed_up.append(activity.id)

    if request.method == 'GET':
        context = {
            'activities': activities,
            'thumbnails': thumbnails,
            'day_of_week': day_of_week,
            'signed_up': signed_up,
        }
        return render(request, 'app/list_volunteering.html', context)

def volunteering_details(request, activity_id):
    """
        This view function renders the detail page for a specific volunteering event after checking to ensure the event exists and/or has not been deleted.
    """
    # ensure activity exists or has not been deleted using activity[0]
    activity = Activity.objects.filter(pk=activity_id)

    try:
        activity = activity[0]

        # identify which thumbnail to pass into template (function requires an iterable arg)
        activity_list = [activity]
        thumbnail = determine_thumbnail(activity_list)
        thumbnail_url = thumbnail[activity_id]

        # get day of week for use with date listing
        day_of_week = datetime.datetime.strptime(str(activity.date), '%Y-%m-%d').strftime('%a')

        # get list of volunteers signed up for this activity using join table instances
        activity_volunteer_instances = activity.activityvolunteer_set.all()
        volunteer_list = list()

        if len(activity_volunteer_instances) is not None:
            for instance in activity_volunteer_instances:
                volunteer_list.append(instance.volunteer)

        # check if there is a user. if so, find out if they're signed up for the activity to give feedback.
        user_is_signed_up = None
        if request.user.is_authenticated:
            user_is_signed_up = check_if_user_is_signed_up(request.user, activity)

        context = {
            'activity': activity,
            'thumbnail_url': thumbnail_url,
            'day_of_week': day_of_week,
            'user_is_signed_up': user_is_signed_up,
            'volunteers': volunteer_list, # Note that this is actuall a list of CustomUser instances...
            'volunteer_count': len(volunteer_list) if volunteer_list is not None else 0
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

        if request.method == 'GET':
            # TODO: instance
            activity_data = {
                'activity': activity.activity,
                'date': activity.date,
                'description': activity.description,
                'start_time': activity.start_time,
                'end_time': activity.end_time,
                'activity_type': activity.activity_type,
                'max_attendance': activity.max_attendance,
            }

            # pre-populate form using dictionary data
            activity_form = ActivityForm(data=activity_data)

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

@login_required
def volunteering_signup(request, activity_id):
    """
        This view function checks to ensure the desired volunteering event exists, is not cancelled, and is upcoming (otherwise it redirects user), then signs up a user instantly for the volunteering event.
    """

    now = datetime.datetime.now()
    activity = Activity.objects.filter(pk=activity_id).filter(date__gte=now).filter(cancelled=None)

    try:
        activity = activity[0]

        if request.method == 'GET':

            # if user is not signed up, then sign them up.
            if check_if_user_is_signed_up(request.user, activity) == False:
                join_table = ActivityVolunteer()
                join_table.activity = activity
                join_table.volunteer = request.user
                join_table.save()

                messages.success(request, f'Thanks for signing up to volunteer with us! We\'ll see you at {activity.activity}!')
                return HttpResponseRedirect(reverse('app:list_volunteering'))

            # if user is already signed up, give them a reminder message
            else:
                messages.success(request, 'You\'ve already signed up for this activity. Thank you!')
                return HttpResponseRedirect(reverse('app:volunteering_details', args=(activity_id,)))

        if request.method == 'POST':
            # if user is signed up, then delete join table.
            if check_if_user_is_signed_up(request.user, activity) == True:
                join_table = ActivityVolunteer.objects.get(activity=activity, volunteer=request.user)
                join_table.delete()

                messages.error(request, f'Sorry you can\'t make it to {activity.activity}! We hope you\'ll volunteer with us again soon!')
                return HttpResponseRedirect(reverse('app:list_volunteering'))

            # if user is not already signed up, give them an error message
            else:
                messages.success(request, 'You aren\'t signed up for this activity.')
                return HttpResponseRedirect(reverse('app:volunteering_details', args=(activity_id,)))

    except IndexError:
        messages.error(request, 'The volunteering activity you\'re trying to access does not exist, is full, already took place, or was cancelled!')
        return HttpResponseRedirect(reverse('app:list_volunteering'))

@staff_member_required
def cancel_volunteering(request, activity_id):
    """
        This view function checks to ensure the desired volunteering event exists, is not cancelled, and is upcoming (otherwise it redirects user), then allows an administrator to cancel the activity entirely, which prevents a user from accessing the detail view (preventing sign up is done in the volunteering_signup view).
    """

    now = datetime.datetime.now()
    activity = Activity.objects.filter(pk=activity_id).filter(date__gte=now).filter(cancelled=None)

    try:
        activity = activity[0]

        if request.method == 'GET':
            # identify which thumbnail to pass into template (function requires an iterable arg)
            activity_list = [activity]
            thumbnail = determine_thumbnail(activity_list)
            thumbnail_url = thumbnail[activity_id]

            # get day of week for use with date listing
            day_of_week = datetime.datetime.strptime(str(activity.date), '%Y-%m-%d').strftime('%a')

            context = {
                'activity': activity,
                'day_of_week': day_of_week,
                'thumbnail_url': thumbnail_url,
            }
            return render(request, 'app/cancel_volunteering.html', context)

        if request.method == 'POST':
            activity.cancelled = True
            activity.save()
            return HttpResponseRedirect(reverse('app:list_volunteering'))

    except IndexError:
        messages.error(request, 'The volunteering activity you\'re trying to cancel does not exist, already took place, or was already cancelled.')
        return HttpResponseRedirect(reverse('app:list_volunteering'))