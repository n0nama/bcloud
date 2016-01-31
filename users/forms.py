# -*- coding: utf-8 -*-
from django import forms
from models import Profile, Portfolio, Skills


class ProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        # Making name required
        self.fields['f_name'].required = True
        self.fields['l_name'].required = True
        self.fields['bd_day'].required = True
        self.fields['bd_month'].required = True
        self.fields['bd_year'].required = True
        self.fields['city'].required = True
        self.fields['skills'].required = True

    class Meta:
        model = Profile
        exclude = ('user', 'rate', )


class PortfolioForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PortfolioForm, self).__init__(*args, **kwargs)


    class Meta:
        model = Portfolio
        fields = ['title', 'description', 'link', 'image']
