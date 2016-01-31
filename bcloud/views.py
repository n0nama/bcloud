from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render

def home(request):
    return render(request, "index.html")
def dashboard(request):
    return render(request, "dashboard.html")