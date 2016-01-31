# coding=utf-8

from rest_framework import serializers
#from models import Profile, Portfolio, Skills, Attach
from users.models import Profile
from django.contrib.auth.models import User

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('f_name', 'l_name', 'bd_day', 'bd_month', 'bd_year', 'spec', 'company', 'rate', 'skills', 'bill_rate', 'website', 'about', 'city', 'avatar', 'filled')
        depth = 1

class UsersSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'profile', 'is_staff')