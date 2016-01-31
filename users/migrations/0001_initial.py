# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import users.storage


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=b'67', blank=True)),
                ('description', models.TextField(blank=True)),
                ('link', models.URLField(blank=True)),
                ('image', models.ImageField(upload_to=b'portfolios/', blank=True)),
                ('thumbnail', models.ImageField(upload_to=b'portfolios/', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('f_name', models.CharField(max_length=b'30', blank=True)),
                ('l_name', models.CharField(max_length=b'30', blank=True)),
                ('birth_date', models.DateField(null=True, blank=True)),
                ('bd_day', models.CharField(max_length=b'2', blank=True)),
                ('bd_month', models.CharField(blank=True, max_length=b'2', choices=[(b'01', b'\xd0\xaf\xd0\xbd\xd0\xb2\xd0\xb0\xd1\x80\xd1\x8c'), (b'02', b'\xd0\xa4\xd0\xb5\xd0\xb2\xd1\x80\xd0\xb0\xd0\xbb\xd1\x8c'), (b'03', b'\xd0\x9c\xd0\xb0\xd1\x80\xd1\x82'), (b'04', b'\xd0\x90\xd0\xbf\xd1\x80\xd0\xb5\xd0\xbb\xd1\x8c'), (b'05', b'\xd0\x9c\xd0\xb0\xd0\xb9'), (b'06', b'\xd0\x98\xd1\x8e\xd0\xbd\xd1\x8c'), (b'07', b'\xd0\x98\xd1\x8e\xd0\xbb\xd1\x8c'), (b'08', b'\xd0\x90\xd0\xb2\xd0\xb3\xd1\x83\xd1\x81\xd1\x82'), (b'09', b'\xd0\xa1\xd0\xb5\xd0\xbd\xd1\x82\xd1\x8f\xd0\xb1\xd1\x80\xd1\x8c'), (b'10', b'\xd0\x9e\xd0\xba\xd1\x82\xd1\x8f\xd0\xb1\xd1\x80\xd1\x8c'), (b'11', b'\xd0\x9d\xd0\xbe\xd1\x8f\xd0\xb1\xd1\x80\xd1\x8c'), (b'12', b'\xd0\x94\xd0\xb5\xd0\xba\xd0\xb0\xd0\xb1\xd1\x80\xd1\x8c')])),
                ('bd_year', models.CharField(max_length=b'4', blank=True)),
                ('company', models.CharField(max_length=b'30', blank=True)),
                ('rate', models.FloatField(default=0.0, null=True, blank=True)),
                ('bill_rate', models.CharField(max_length=b'255', blank=True)),
                ('contacts', models.CharField(max_length=b'255', blank=True)),
                ('website', models.URLField(blank=True)),
                ('about', models.TextField(blank=True)),
                ('city', models.CharField(max_length=b'127', blank=True)),
                ('avatar', models.ImageField(default=b'/static/img/avatars/d_av.png', storage=users.storage.FSS(), upload_to=b'avatars/', blank=True)),
                ('filled', models.BooleanField(default=False)),
                ('modified', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Skills',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tags', models.CharField(max_length=b'255', null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='skills',
            field=models.ForeignKey(to='users.Skills', null=True),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
