# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from django import forms
from models import Profile
import settings
import re
import base64


class CalendarWidget(forms.TextInput):

    class Meta:
        css = {
            'all': ('/ui/datepicker/dp.css',),
        }
        js = ('/ui/datepicker/dp.js')


class ProfileForm(forms.ModelForm):
        
    class Meta:
        model = Profile
        exclude = ('user', 'rate', 'portfolio', )

    def __init__(self, user, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['f_name'].widget = forms.TextInput(attrs={'class': settings.INPUT_CLASS, 'value': user.profile.f_name})
        self.fields['f_name'].label = _("Name"),
        self.fields['l_name'].widget = forms.TextInput(attrs={'class': settings.INPUT_CLASS, 'value': user.profile.l_name})
        self.fields['l_name'].label = _("Last Name"),
        self.fields['birth_date'].widget = CalendarWidget(attrs={'class': settings.INPUT_CLASS, 'value': user.profile.birth_date})
        self.fields['birth_date'].label = _("Age"),
        self.fields['company'].widget = forms.TextInput(attrs={'class': settings.INPUT_CLASS, 'value': user.profile.company})
        self.fields['company'].label = _("Company"),
        self.fields['skills'].widget = forms.TextInput(attrs={'class': settings.INPUT_CLASS, 'value': user.profile.skills})
        self.fields['skills'].label = _("Skills"),
        self.fields['bill_rate'].widget = forms.TextInput(attrs={'class': settings.INPUT_CLASS, 'value': user.profile.bill_rate})
        self.fields['bill_rate'].label = _("Bill rate"),
        self.fields['contacts'].widget = forms.TextInput(attrs={'class': settings.INPUT_CLASS, 'value': user.profile.contacts})
        self.fields['contacts'].label = _("Contacts"),
        self.fields['avatar'].widget = forms.TextInput(attrs={'class': settings.AVATAR_CLASS, 'value': user.profile.avatar})
        self.fields['avatar'].label = _(" "),

    def save(self, user):
        obj = super(ProfileForm, self).save(commit=False)
        obj.user = user
        return obj.save()
"""
class AvatarForm(forms.ModelForm):
	
	class Meta:
		model = Profile
		fields = ('avatar', )
"""