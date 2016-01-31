# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatUser',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='room',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('room_id', models.TextField()),
                ('room_name', models.CharField(default=b'', max_length=30)),
                ('users', models.ManyToManyField(to='chat.ChatUser', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='message',
            name='room',
            field=models.ForeignKey(related_name='room', to='chat.room'),
        ),
        migrations.AddField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(related_name='sender', to='chat.ChatUser'),
        ),
        migrations.AddField(
            model_name='chatuser',
            name='dialogs',
            field=models.ManyToManyField(to='chat.room', blank=True),
        ),
        migrations.AddField(
            model_name='chatuser',
            name='friends',
            field=models.ManyToManyField(related_name='friends_rel_+', to='chat.ChatUser', blank=True),
        ),
    ]
