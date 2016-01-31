# coding=utf-8
from django import forms
from django.forms import ModelForm

from .models import Project, Attachment, Reply
from .models import PRIVACY, STATUS


class CreateProjectForm(ModelForm):

    class Meta:
        model = Project
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'})
        }
        exclude = [
            'project_id',
            'author',
            'pub_date',
            'modified',
            'progress',
            'status',
        ]


class AddProjectAttachmentForm(ModelForm):

    class Meta:
        model = Attachment
        exclude = [
            'upload_date'
        ]


class PerformersReplyForm(ModelForm):

    class Meta:
        model = Reply
        exclude = [
            'project',
            'author',
            'pub_date'
        ]


class FilterStatusForm(forms.Form):
    status = STATUS + (('*', 'Все'),)
    status_type = forms.ChoiceField(choices=status)
