from django.urls import path
from . import views

app_name = "app"
urlpatterns = [
    # ex. /
    path("", views.index, name='index'),
    # ex. /login
    path("login", views.login_user, name='login'),
    # ex. /logout
    path("logout", views.logout_user, name='logout'),
    # ex. /register
    path("register", views.register, name='register'),
    # ex. /profile
    path("profile", views.profile, name='profile'),
    # ex. /pets
    path("pets", views.available_animals, name='pets'),
    # ex. /pets/details/1
    path("pets/details/<int:id>", views.animal_detail, name='animal_detail'),
    # ex. /new_arrival
    path("new_arrival", views.new_arrival, name='new_arrival'),
    # ex. /pets/adopt/1
    path("pets/adopt/<int:id>", views.adoption_app, name='adopt'),
]