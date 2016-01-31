# -*- coding: utf-8 -*-

from django.contrib import admin
from models import Project, Entry, EntryAttach, Reply, Attachment, Skill
from django.contrib.auth.models import User


class AttachmentAdmin(admin.TabularInline):
    model = Attachment
    extra = 1
    can_delete = True


class ProjectAdmin(admin.ModelAdmin):

    inlines = [AttachmentAdmin]

    list_per_page = 25

admin.site.register(Project, ProjectAdmin)
admin.site.register(Reply)
admin.site.register(Entry)
admin.site.register(Skill)