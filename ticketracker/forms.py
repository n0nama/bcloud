 # -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm
from .models import Ticket, TicketFile, TicketComment
from django.db.models import F

STATUS_CHOICE = Ticket.STATUS_CHOICE

# Форма для создания нового тикета
class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        #fields = ['title','body', 'classification']
        exclude = ['open_date', 'close_date', 'author', 'status', 'classification', 'responsible_person', 'depend_from']
        
class UploadFileForm(ModelForm):
    class Meta:
        model = TicketFile
        exclude = ['ticket']
