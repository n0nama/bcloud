 # -*By- coding: utf-8 -*-

from django.db import models

from django.db.models import signals
from django.dispatch import receiver

from django.contrib.auth.models import User

from time import time
from django.utils import timezone

from django.utils.safestring import mark_safe

def upload_file_name(instance, filename):
    #return '%s/%s' % (instance.ticket.id, filename)       
    return 'ticket/%s/%s_%s' % (instance.ticket.id, str(time()).replace('.','_'), filename)

class Ticket(models.Model):
    title = models.CharField(verbose_name=u'*Заголовок', max_length=30)
    body = models.TextField(verbose_name=u'*Описание проблемы')
    open_date = models.DateTimeField(verbose_name=u'Дата открытия', auto_now_add=True)
    close_date = models.DateTimeField(verbose_name=u'Дата закрытия', null=True, blank=True)
    author = models.ForeignKey(User, verbose_name=u'Сообщил')
    author_email = models.EmailField(verbose_name='*e-mail')
    responsible_person = models.ForeignKey(User, related_name='responsible_person', null=True, blank=True, verbose_name=u'Ответственный')
    STATUS_CHOICE = (
        ('o', 'Открыт'),
        ('c', 'Закрыт'),
        ('m', 'Под наблюдением'),
    )
    '''По умолчанию все тикеты не имеют responsible_person_id'''
    status = models.CharField(verbose_name=u'Статус', max_length = 1,
                              choices = STATUS_CHOICE,
                              default ='o')
    
    classification = models.BooleanField('Общая проблема', default=False)
    depend_from = models.PositiveIntegerField(null=True, blank=True)
    
    def __unicode__(self):
        return self.title
      
    def is_ticket_open(self):
        return self.status == 'o'

    def does_close_date(self):
        if self.close_date == None:
            return u'Тикет еще не закрыт'
        else:
            return self.close_date

    
    is_ticket_open.short_description = u'Тикет открыт?'
    is_ticket_open.boolean = True

    does_close_date.short_description = u"Дата закрытия"
    
class TicketComment(models.Model):
    author = models.ForeignKey(User)
    ticket = models.ForeignKey(Ticket)
    body = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    
class TicketFile(models.Model):
    ticket = models.ForeignKey(Ticket)
    upload_file = models.FileField(upload_to=upload_file_name, blank=True, verbose_name=u'Приложить файл') 
    
'''
При закрытие тикета изменить дату закрытия на текущее время
'''
@receiver(signals.pre_save, sender=Ticket)
def modify_close_date(sender, instance, **kwargs):
    if (instance.close_date == None or instance.close_date < timezone.now()) and instance.status == 'c':
        instance.close_date = timezone.now()

# signals.pre_save.connect(modify_close_date, sender=Ticket)'''

'''
Если изменяем статус общего тикета, то должнен измениться и статус прикрепленных тикетов.
Если у прикрепленного тикета нет responsible_person, то это поле меняется на того, кто изменил состояние тикета.
'''
@receiver(signals.post_save, sender=Ticket)
def chose_dependent_ticket_status(sender, instance, **kwargs):
    if instance.classification:
        dependent_tickets = Ticket.objects.filter(depend_from=instance.id)
        for tt in dependent_tickets:
            if tt.responsible_person_id == None:
                tt.responsible_person_id = instance.responsible_person_id
            tt.status = instance.status
            tt.save()

'''
Если файл не добавлен, убрать пустую строку из БД
'''
@receiver(signals.post_save, sender=TicketFile)
def delete_blank_file_field(sender, instance, **kwargs):
    if (instance.upload_file == '' or instance.upload_file == None):
        instance.delete()
        