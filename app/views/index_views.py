from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template import RequestContext

def index(request):
    return render(request, 'app/index.html', {})