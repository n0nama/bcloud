 # -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from .models import Ticket, TicketFile
from .forms import TicketForm, UploadFileForm
from django.core.context_processors import csrf
from django.utils import timezone


def complain(request):
    args = {}
    args['user'] = request.user
    return render_to_response('complain.html', args)

def add_ticket(request):
    if request.method == "POST":
        ticket_form = TicketForm(request.POST, instance=Ticket())
        file_form = [UploadFileForm(request.POST, request.FILES, prefix=str(x), instance=TicketFile()) for x in range(0,3)]
        if ticket_form.is_valid() and all([ff.is_valid() for ff in file_form]):
            # Создаем instance form, но не сохраняем его, т.к. нужно добавить автора
            form = ticket_form.save(commit=False)
            # Добавляем автора сообщения в форму. Автор должен быть зарегестрирован в системе
            form.author_id = request.user.id
            form.save()
            for ff in file_form:
                new_file = ff.save(commit=False)
                new_file.ticket = form
                new_file.save()

            return render_to_response('ticket_accepted.html')
        else:
            return ('Не верно заполнены поля.')
    else:
        ticket_form = TicketForm(instance=Ticket())
        file_form = [UploadFileForm(prefix=str(x), instance=TicketFile()) for x in range(0,3)]
        
        args = {}
        args.update(csrf(request))
        args['ticket_form'] = ticket_form
        args['file_form'] = file_form
        return render_to_response('add_ticket.html', args)