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

# messages
from django.contrib import messages
# tools
import datetime

def list_volunteering(request):

    now = datetime.datetime.now()
    activities = Activity.objects.filter(date_end__lte=now)

    if request.method == 'GET':
        context = {
            'activities': activities,
        }
        return render(request, 'app/list_volunteering.html', context)