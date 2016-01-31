# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20150901_1122'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='spec',
            field=models.CharField(max_length=b'30', blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='skills',
            field=models.ManyToManyField(related_name='skills', null=True, to='users.Skills'),
        ),
    ]
