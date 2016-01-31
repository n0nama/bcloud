# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

STATUS = (
    ('II', 'Важная информация'),
    ('IN', 'Стандартная запись'),
    ('BU', 'Исправление ошибок'),
    ('UP', 'Обновление'),
)


class New(models.Model):
    title = models.CharField(max_length = 128)
    text = models.TextField()
    status = models.CharField(blank=True, choices=STATUS, max_length='2')
    marked = models.BooleanField(default=False)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title



class Attach(models.Model):
    new = models.ForeignKey(New, null = True, related_name='attach')
    att = models.FileField(upload_to='news/', blank = True)

    def __unicode__(self):
        return self.new.title


class Comment(models.Model):
    new = models.ForeignKey(New, null = True, related_name='comments')
    author = models.ForeignKey(User, related_name='author')
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.new.title


class Reply(models.Model):
    comment = models.ForeignKey(Comment, null = True, related_name='replies')
    staff = models.ForeignKey(User, related_name='staff')
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)