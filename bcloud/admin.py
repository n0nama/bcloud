# -*- coding: utf-8 -*-

import psutil
from django.contrib import admin
from ticketracker.models import Ticket
from news.models import Comment
from django.utils import timezone
from django.conf.urls import patterns, include, url
from django.shortcuts import render

def dash(request):
    ntic = Ticket.objects.exclude(status='c')
    ram_per = psutil.virtual_memory().percent
    cpu_per = psutil.cpu_percent(interval=0)
    sdd_per = psutil.disk_usage('/').percent
    comments = Comment.objects.select_related().filter(replies=None)
    try:
        mytic = Ticket.objects.filter(responsible_person=request.user.id).values()
        ctic = Ticket.objects.filter(status='c').values()
    except:
        mytic = {}
        ctic = {}
    return render(request, "dash.html", {'ntic':ntic, 'mytic':mytic, 'ctic':ctic, 'ram': ram_per, 'cpu': cpu_per, 'sdd': sdd_per, 'comments' : comments})