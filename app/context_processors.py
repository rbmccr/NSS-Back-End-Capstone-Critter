# models
from .models import Application

def pending_app_count(request):
    count = 0
    if request.user.is_staff:

        pending_apps = Application.objects.filter(approved=None)
        if len(pending_apps) > 0:
            for app in pending_apps:
                count += 1

        return {'pending_app_count': count}


