# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messag', '0001_initial'),
    ]

    operations = [
         migrations.CreateModel(
            name='DraftMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(max_length=120, verbose_name='Subject')),
                ('body', models.TextField(verbose_name='Body')),
                ('recipient', models.CharField(max_length=300, verbose_name='Recipient draft')),
                ('sender', models.ForeignKey(related_name='sent_messages_draft', verbose_name='Sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='draftmessage',
            name='edited_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
