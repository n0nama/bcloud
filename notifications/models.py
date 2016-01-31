from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
import redis
import json

NOTIFICATION_TYPES = (
    ('M', 'Messages'),
    ('I', 'Invite'),
)


class Notification(models.Model):
    user = models.ForeignKey(User)
    type = models.CharField(max_length=3, choices=NOTIFICATION_TYPES, blank=True, null=True)
    body = models.TextField()
    link = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def serialize(self):
        message = {'type': self.type, 'body': self.body, 'id': self.id}
        if self.link is not None:
            message['link'] = self.link
        return message


@receiver(post_save, sender=Notification)
def send_notification(instance, **kwargs):
    message = json.dumps({'id': instance.id})
    r = redis.StrictRedis(host='127.0.0.1', port=6379)
    r.publish(instance.user.id, message)