# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from datetime import datetime
from storage import FSS

s = FSS()

MONTHS = (
    ('01', 'Январь'),
    ('02', 'Февраль'),
    ('03', 'Март'),
    ('04', 'Апрель'),
    ('05', 'Май'),
    ('06', 'Июнь'),
    ('07', 'Июль'),
    ('08', 'Август'),
    ('09', 'Сентябрь'),
    ('10', 'Октябрь'),
    ('11', 'Ноябрь'),
    ('12', 'Декабрь'),
)

class Skills(models.Model):
    tags = models.CharField(max_length='255', blank=True, null=True)

    def __unicode__(self):
        return self.tags


class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    f_name = models.CharField(blank=True, max_length='30')
    l_name = models.CharField(blank=True, max_length='30')
    bd_day = models.CharField(blank=True, max_length='2')
    bd_month = models.CharField(blank=True, choices=MONTHS, max_length='2')
    bd_year = models.CharField(blank=True, max_length='4')
    spec = models.CharField(blank=True, max_length='30')
    company = models.CharField(blank=True, max_length='30')
    rate = models.FloatField(null=True, blank=True, default=0.0)
    skills = models.ManyToManyField(Skills, related_name='skills')
    bill_rate = models.CharField(blank=True, max_length='255')
    website = models.URLField(blank=True)
    about = models.TextField(blank=True)
    city = models.CharField(blank=True, max_length='127')
    avatar = models.ImageField(upload_to='avatars/', blank = True, default='/static/img/avatars/d_av.png', storage=s)
    filled = models.BooleanField(default=False)
    modified = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.user.username
    
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    post_save.connect(create_user_profile, sender=User)


class Portfolio(models.Model):
    user = models.ForeignKey(Profile)
    title = models.CharField(blank = True, max_length='67')
    description = models.TextField(blank=True)
    link = models.URLField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.user.user.username
        

class Attach(models.Model):
    portfolio = models.ForeignKey(Portfolio, related_name='attach')
    att = models.FileField(upload_to='portfolios/', blank = True)

    def __unicode__(self):
        return self.att.url