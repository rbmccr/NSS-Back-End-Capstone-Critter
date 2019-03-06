from django.contrib import admin
from .models import *

admin.site.register(CustomUser)
admin.site.register(Volunteer)
admin.site.register(Animal)
admin.site.register(Breed)
admin.site.register(Color)
admin.site.register(Species)
admin.site.register(Application)