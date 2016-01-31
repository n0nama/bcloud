# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='new',
            name='attach',
        ),
        migrations.AddField(
            model_name='attach',
            name='new',
            field=models.ForeignKey(related_name='attach', to='news.New', null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='new',
            field=models.ForeignKey(related_name='comments', to='news.New', null=True),
        ),
        migrations.AlterField(
            model_name='reply',
            name='comment',
            field=models.ForeignKey(related_name='replies', to='news.Comment', null=True),
        ),
    ]
