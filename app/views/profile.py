from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.models import User
from app.forms import UserForm, VolunteerForm

@login_required
def profile(request):

    if request.method == 'GET':
        user = request.user
        user_form = UserForm()
        volunteer_form = VolunteerForm()
        context = {'user': user, 'user_form': user_form, 'volunteer_form': volunteer_form}
        return render(request, 'app/profile.html', context)

    # elif request.method == "POST":

    #     if 'edit' in request.POST:
    #         user = request.user
    #         form = {"formA": UserCustomerFormA(instance = user), "formB": UserCustomerFormB(instance = user.customer)}
    #         context = {"user": request.user,
    #                     "form": form}
    #         return render(request, 'customer_profile.html', context)

    #     else:
    #         req=request.POST
    #         form_user = {"last_name": req["last_name"]}
    #         form_cust = {"phone_number": req["phone_number"], "street_address": req["street_address"], "city": req["city"], "state": req["state"], "zipcode": req["zipcode"]}


    #         user_form = UserCustomerFormA(form_user)

    #         if user_form.is_valid():
    #             with connection.cursor() as cursor:
    #                 cursor.execute("UPDATE auth_user SET last_name=%s WHERE id=%s", [req["last_name"], request.user.id])

    #         customer_form = UserCustomerFormB(form_cust)

    #         if customer_form.is_valid():
    #             with connection.cursor() as cursor:
    #                 cursor.execute("UPDATE website_customer SET phone_number=%s, street_address=%s, city=%s, state=%s, zipcode=%s WHERE id=%s", [req["phone_number"], req["street_address"], req["city"], req["state"], req["zipcode"], request.user.customer.id])


    #         user = User.objects.raw("Select * From auth_user where id=%s",[request.user.id])
    #         context = {"user": user[0]}
    #         return render(request, 'customer_profile.html', context)