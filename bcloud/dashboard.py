 # -*- coding: utf-8 -*-
"""
This file was generated with the customdashboard management command, it
contains the two classes for the main dashboard and app index dashboard.
You can customize these classes as you want.

To activate your index dashboard add the following to your settings.py::
    ADMIN_TOOLS_INDEX_DASHBOARD = 'business_cloud.dashboard.CustomIndexDashboard'

And to activate the app index dashboard::
    ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'business_cloud.dashboard.CustomAppIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools.utils import get_admin_site_name
from ticketracker import views
from ticketracker.models import Ticket

'''class MyTicketsModule(modules.LinkList):
    #title = u'Мои тикеты'
    def __init__ (self, **kwargs):
        super (MyTicketsModule, self).__init__(**kwargs)
        self.title = u'Мои тикеты'
        #self.template = 'myticketsmodule/tickets.html
    
    def init_with_context(self, context):
        request = context['request']
        tickets = Ticket.objects.all()
        for ticket in tickets:
            if request.user.is_authenticated():
                if request.user.username == ticket.responsible_person.username:
                    self.children.append([ticket.title, 'ticketracker/ticket/%s/'%ticket.id])
                    #self.children.append([(ticket.title), '/ticketracker/ticket/52/', False])'''
    
                
                   
class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for business_cloud.
    """
    columns = 2
    def __init__(self, **kwargs):
        Dashboard.__init__(self, **kwargs)
        self.children.append(modules.Group(
        title = _(u'Основное'),
        display = 'tabs',
        children = [
            modules.AppList(
                title = u'Тикеты',
                models = ('ticketracker.*',)
            ),
            modules.AppList(
                title = u'Пользователи',
                models = ('django.contrib.auth.models.User','django.contrib.auth.models.Group') #'django.contrib.auth.models.*
            ),
                
        ]
        ))

    '''
    createMyTicketsList создает список списков [[],[], и т.д], каждый из которых состоит из Названия тикета и ссылке на тикет.
    Список заполняется тикетами, поле responsible_persone которых совпадает с залогиненым пользователем. При создании нового тикета поле responsible_persone = none
    и тикет считается новым. Залогиненый пользователь береться из context. Параметром stasus
    определяем нужный нам статус тикета. status == 'close' для закрытых тикетов, 'new' для новых  и 'open' для всех остальных
    '''
    def createMyTicketsList(self, context, status):
        request = context['request']
        tickets = Ticket.objects.order_by('-open_date')
        #tickets = Ticket.objects.all()
        myTicketsList = []
        for ticket in tickets:
            if request.user.is_authenticated() and request.user.is_staff:
                
                if ticket.responsible_person_id == None:
                    if status == 'new': 
                        myTicketsList.append([(u'Номер:%s. Статус: %s'%(ticket.id, ticket.get_status_display())), 'ticketracker/ticket/%s/'%ticket.id])
                elif ticket.responsible_person_id !=None:
                    if status == 'open':# or status == 'monitor':
                        if (request.user.username == ticket.responsible_person.username and ticket.status != 'c' and not ticket.classification):
                            myTicketsList.append([(u'Номер:%s. Статус: %s'%(ticket.id, ticket.get_status_display())), 'ticketracker/ticket/%s/'%ticket.id])
                    elif status == 'close':
                        if request.user.username == ticket.responsible_person.username and ticket.status == 'c':
                            myTicketsList.append([(u'Номер:%s. Статус: %s'%(ticket.id, ticket.get_status_display())), 'ticketracker/ticket/%s/'%ticket.id])
                    elif status == 'main' and ticket.classification and ticket.status != 'c':
                        myTicketsList.append([(u'Номер:%s. Статус: %s, Ответственный: %s'%(ticket.id, ticket.get_status_display(), ticket.responsible_person)), 'ticketracker/ticket/%s/'%ticket.id])
                

        if myTicketsList == []:
            myTicketsList.append(['Ничего пока нет','ticketracker/ticket/'])
        return myTicketsList
    
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
        # append a link list module for "quick links"
        #myTicketsList = self.createMyTicketsList(context)
        self.children.append(modules.LinkList(
            _(u'Быстрые ссылки'),
            layout='inline',
            draggable=False,
            deletable=False,
            collapsible=False,
            children=[
                
                [_(u'Перейти на сайт'), '/', False,'Главная страница'],
                [_(u'Сменить пароль'), reverse('%s:password_change' % site_name)],
                [_(u'Выйти'), reverse('%s:logout' % site_name)],
                ###[_(u'Тикеты'), reverse('ticketracker:ticketracker_all_tickets')]
            ]
        ))

        self.children.append(modules.LinkList(
            _(u'Общие проблемы'),
            deletable=False,
            # в children передаем список тикетов для нужного responsible_persone            
            children = self.createMyTicketsList(context, 'main')
        ))
        
        self.children.append(modules.LinkList(
            _(u'Новые'),
            deletable=False,
            children = self.createMyTicketsList(context, 'new')
        ))
        
        self.children.append(modules.LinkList(
            _(u'Мои открытые тикеты'),
            #layout='inline',
            #draggable=False,
            deletable=False,
            #collapsible=False,
            # в children передаем список тикетов для нужного responsible_persone            
            children = self.createMyTicketsList(context, 'open')
        ))
        
        self.children.append(modules.LinkList(
            _(u'Мои закрытые тикеты'),
            #layout='inline',
            #draggable=False,
            #deletable=False,
            #collapsible=False,
            # в children передаем список тикетов для нужного responsible_persone            
            children = self.createMyTicketsList(context, 'close')
        ))

        #append another link list module for "support".
        #self.children.append(MyTicketsModule())
        '''
        self.children.append(modules.LinkList(
            _('Support'),
            children=[
                {
                    'title': _('Django documentation'),
                    'url': 'http://docs.djangoproject.com/',
                    'external': True,
                },
                {
                    'title': _('Django "django-users" mailing list'),
                    'url': 'http://groups.google.com/group/django-users',
                    'external': True,
                },
                {
                    'title': _('Django irc channel'),
                    'url': 'irc://irc.freenode.net/django',
                    'external': True,
                },
            ]
        ))

        # append an app list module for "Applications"
        self.children.append(modules.AppList(
            _('Applications'),
            exclude=('django.contrib.*',),
        ))

        # append an app list module for "Administration"
        self.children.append(modules.AppList(
            _('Administration'),
            models=('django.contrib.*',),
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(_('Recent Actions'), 5))

        # append a feed module
        self.children.append(modules.Feed(
            _('Latest Django News'),
            feed_url='http://www.djangoproject.com/rss/weblog/',
            limit=5
        ))
        '''

class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for business_cloud.
    """

    # we disable title because its redundant with the model list module
    title = ''

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # append a model list module and a recent actions module
        self.children += [
            modules.ModelList(self.app_title, self.models),
            #modules.RecentActions(
            #    _('Recent Actions'),
            #    include_list=self.get_app_content_types(),
            #    limit=5
            #)
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomAppIndexDashboard, self).init_with_context(context)
