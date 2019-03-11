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
    # ex. /profile/edit
    path("profile/edit", views.edit_profile, name='edit_profile'),
    # ex. /profile/edit
    path("profile/edit/password", views.change_password, name='change_password'),
    # ex. /pets
    path("pets", views.available_animals, name='pets'),
    # ex. /pets/search
    path("pets/search", views.available_animals_search, name='search_pets'),
    # ex. /pets/details/1
    path("pets/details/<int:id>", views.animal_detail, name='animal_detail'),
    # ex. /new_arrival
    path("new_arrival", views.new_arrival, name='new_arrival'),
    # ex. /pets/adopt/1
    path("pets/adopt/<int:id>", views.adoption_app, name='adopt'),
    # ex. /adoptions/all
    path("adoptions/all", views.list_applications, name='list_applications'),
    # ex. /adoptions/1
    path("adoptions/pet/<int:id>", views.list_specific_applications, name='list_specific_applications'),
    # ex. /adoptions/1/final
    path("adoptions/pet/<int:animal_id>/final/app_id=<int:application_id>", views.final_decision, name='final_decision'),
    # ex. /adoptions/1/final/reject/app_id=1
    path("adoptions/pet/<int:animal_id>/reject/app_id=<int:application_id>", views.reject_application, name='reject_application'),
    # ex. /adoptions/1/final/revise/app_id=1
    path("adoptions/pet/<int:animal_id>/revise/app_id=<int:application_id>", views.revise_judgment, name='revise_judgment'),
]