from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from users.models import Profile
import random
from django.utils.crypto import get_random_string


class ChatUser(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    friends = models.ManyToManyField('self', blank=True)
    dialogs = models.ManyToManyField('room', blank=True)

    def __unicode__(self):
        return self.user.username

    def create_ChatUser(sender, instance, created, **kwargs):
        if created:
            ChatUser.objects.create(user=instance)

    post_save.connect(create_ChatUser, sender=User)


class room(models.Model):
    room_id   = models.TextField()
    users     = models.ManyToManyField('ChatUser', blank=True)
    room_name = models.CharField(max_length=30, default='')

    def set_id(self):
        while True:
            id = random.randint(100000,1000000)
            if len(room.objects.filter(room_id=id)) == 0:
                self.room_id = id
                break

    def __unicode__(self):
        return self.room_name



class message(models.Model):
    sender = models.ForeignKey('ChatUser', related_name = 'sender')
    room   = models.ForeignKey('room', related_name='room')
    text   = models.TextField()
    date   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['date']

    def __unicode__(self):
        return self.text

    def get_date(self):
        hour   = str(self.date.hour)
        minute = str(self.date.minute)
        if len(minute) == 1:
            minute = '0' + minute
        return hour+':'+minute

    def get_fname(self):
        return Profile.objects.get(user=self.sender.user).f_name