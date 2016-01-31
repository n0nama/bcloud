 # -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Ticket, TicketFile, TicketComment
from django.utils import timezone
from django.contrib.auth.models import User



class TicketCommentAdmin(admin.TabularInline):
    model = TicketComment
    extra = 1
    can_delete = False

class TicketFileAdmin(admin.TabularInline):
    model = TicketFile
    extra = 1
    can_delete = False

class TicketAdmin(admin.ModelAdmin):
   
    actions = ['close_selected_tickets']
    
    def close_selected_tickets(self, request, queryset):
        queryset.update(status='c')
        queryset.update(close_date = timezone.now())
    close_selected_tickets.short_description = u"Закрыти все выбранные тикеты"

    fieldsets = [
        (None, {
            'fields':['author','author_email']
        }),
        (u'Описание', {
            'classes': ['extrapretty',], 
            'fields': ['title', 'body']
        }),
        (u'Служебное', {
            'fields':['responsible_person', 'status', 'classification', 'depend_from']
        }),
    ]
    
    inlines = [TicketFileAdmin, TicketCommentAdmin]
    
    list_display = ('id', 'title', 'open_date', 'does_close_date', 'is_ticket_open')
    
    list_display_links = ('id', 'title', 'open_date', 'does_close_date', 'is_ticket_open')
    
    list_filter = ('open_date', 'close_date')

    search_fields = ['title', 'body']
    
    list_per_page = 25

admin.site.register(Ticket, TicketAdmin)