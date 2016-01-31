# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from users.models import Profile

import datetime

STATUS = (('N', 'Новый'), ('I', 'В разработке'), ('F', 'На удержании'), ('D', 'Черновик'), ('C', 'Закрыт'),)
PRIVACY = (('PU', 'Общий'), ('PR', 'Персональный'),)
CTYPE = (('D', 'Договорная'), ('A', 'Предусмотрен аванс'), ('F', 'Оплата по факту'),)
ETYPE = (('U', 'Обновление'), ('Q', 'Вопрос'), ('I', 'На заметку'), ('E', 'Исправление ошибки'))


class Skill(models.Model):
    skill = models.CharField(max_length=50)

    def __unicode__(self):
        return self.skill


class Project(models.Model):

    project_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, related_name='author_id')
    title = models.CharField(max_length='255')
    description = models.TextField()
    performers = models.ManyToManyField(User, blank=True)  # development team (?)
    privacy_type = models.CharField(max_length='2', choices=PRIVACY)
    skill_req = models.ManyToManyField(Skill)  # required skills
    complex_lvl = models.PositiveSmallIntegerField(default=0) # complexity level
    pub_date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    modified = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length='1', choices=STATUS, default='N')
    progress = models.PositiveSmallIntegerField(default=0)  # percentage
    compensation = models.DecimalField(max_digits=12, decimal_places=2)
    compensation_type = models.CharField(max_length='1', choices=CTYPE)
    marked = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title


class Attachment(models.Model):
    project = models.ForeignKey(Project)
    upload_file = models.FileField(upload_to='attachements/', blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.project.title


class Entry(models.Model):
    project = models.ForeignKey(Project, unique=True, null=True)
    person = models.ForeignKey(User, unique=True, null=True)
    text = models.TextField()
    e_type = models.CharField(max_length='1', choices=ETYPE)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.text


class EntryAttach(models.Model):
    entry = models.ForeignKey(Entry)
    upload_file = models.FileField(upload_to='attachements/', blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.entry.text


class Reply(models.Model):
    project = models.ForeignKey(Project, null=True)
    author = models.ForeignKey(User, null=True)
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.text
