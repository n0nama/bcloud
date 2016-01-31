# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20150902_1246'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attach',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('att', models.FileField(upload_to=b'portfolios/', blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='portfolio',
            name='thumbnail',
        ),
        migrations.AddField(
            model_name='attach',
            name='portfolio',
            field=models.ForeignKey(related_name='attach', to='users.Portfolio'),
        ),
    ]
