# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('upload_file', models.FileField(null=True, upload_to=b'attachements/', blank=True)),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('e_type', models.CharField(max_length=b'1', choices=[(b'U', b'\xd0\x9e\xd0\xb1\xd0\xbd\xd0\xbe\xd0\xb2\xd0\xbb\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5'), (b'Q', b'\xd0\x92\xd0\xbe\xd0\xbf\xd1\x80\xd0\xbe\xd1\x81'), (b'I', b'\xd0\x9d\xd0\xb0 \xd0\xb7\xd0\xb0\xd0\xbc\xd0\xb5\xd1\x82\xd0\xba\xd1\x83'), (b'E', b'\xd0\x98\xd1\x81\xd0\xbf\xd1\x80\xd0\xb0\xd0\xb2\xd0\xbb\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5 \xd0\xbe\xd1\x88\xd0\xb8\xd0\xb1\xd0\xba\xd0\xb8')])),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('person', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='EntryAttach',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('upload_file', models.FileField(null=True, upload_to=b'attachements/', blank=True)),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('entry', models.ForeignKey(to='projects.Entry')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('project_id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=b'255')),
                ('description', models.TextField()),
                ('privacy_type', models.CharField(max_length=b'2', choices=[(b'PU', b'\xd0\x9e\xd0\xb1\xd1\x89\xd0\xb8\xd0\xb9'), (b'PR', b'\xd0\x9f\xd0\xb5\xd1\x80\xd1\x81\xd0\xbe\xd0\xbd\xd0\xb0\xd0\xbb\xd1\x8c\xd0\xbd\xd1\x8b\xd0\xb9')])),
                ('complex_lvl', models.PositiveSmallIntegerField(default=0)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('deadline', models.DateTimeField()),
                ('modified', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(default=b'N', max_length=b'1', choices=[(b'N', b'\xd0\x9d\xd0\xbe\xd0\xb2\xd1\x8b\xd0\xb9'), (b'I', b'\xd0\x92 \xd1\x80\xd0\xb0\xd0\xb7\xd1\x80\xd0\xb0\xd0\xb1\xd0\xbe\xd1\x82\xd0\xba\xd0\xb5'), (b'F', b'\xd0\x9d\xd0\xb0 \xd1\x83\xd0\xb4\xd0\xb5\xd1\x80\xd0\xb6\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb8'), (b'D', b'\xd0\xa7\xd0\xb5\xd1\x80\xd0\xbd\xd0\xbe\xd0\xb2\xd0\xb8\xd0\xba'), (b'C', b'\xd0\x97\xd0\xb0\xd0\xba\xd1\x80\xd1\x8b\xd1\x82')])),
                ('progress', models.PositiveSmallIntegerField(default=0)),
                ('compensation', models.DecimalField(max_digits=12, decimal_places=2)),
                ('compensation_type', models.CharField(max_length=b'1', choices=[(b'D', b'\xd0\x94\xd0\xbe\xd0\xb3\xd0\xbe\xd0\xb2\xd0\xbe\xd1\x80\xd0\xbd\xd0\xb0\xd1\x8f'), (b'A', b'\xd0\x9f\xd1\x80\xd0\xb5\xd0\xb4\xd1\x83\xd1\x81\xd0\xbc\xd0\xbe\xd1\x82\xd1\x80\xd0\xb5\xd0\xbd \xd0\xb0\xd0\xb2\xd0\xb0\xd0\xbd\xd1\x81'), (b'F', b'\xd0\x9e\xd0\xbf\xd0\xbb\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbf\xd0\xbe \xd1\x84\xd0\xb0\xd0\xba\xd1\x82\xd1\x83')])),
                ('marked', models.BooleanField(default=False)),
                ('author', models.ForeignKey(related_name='author_id', to=settings.AUTH_USER_MODEL)),
                ('performers', models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
                ('project', models.ForeignKey(to='projects.Project', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('skill', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='skill_req',
            field=models.ManyToManyField(to='projects.Skill'),
        ),
        migrations.AddField(
            model_name='entry',
            name='project',
            field=models.ForeignKey(null=True, to='projects.Project', unique=True),
        ),
        migrations.AddField(
            model_name='attachment',
            name='project',
            field=models.ForeignKey(to='projects.Project'),
        ),
    ]
