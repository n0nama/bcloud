# coding=utf-8


import re
import os
import base64, uuid
import tempfile
import settings
from django.core.files.base import File

ROOT_PATH = os.path.join(os.path.dirname(__file__), '..')
PORTFOLIO_DIR = os.path.abspath(ROOT_PATH)

from rest_framework import serializers
from models import Profile, Portfolio, Skills, Attach
from django.contrib.auth.models import User

class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                print('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


class SkillsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skills
        fields = ('id', 'tags')


class SkillsUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=False)

    class Meta:
        model = Skills
        fields = ('id',)


class AttachSerializer(serializers.ModelSerializer):

    class Meta: 
        model = Attach
        fields = ('id', 'portfolio', 'att')
        read_only_fields = ('id')

class PortfolioSerializer(serializers.ModelSerializer):
    attach = AttachSerializer(many=True)
    
    class Meta:
        model = Portfolio
        fields = ('id', 'user', 'title', 'description', 'link', 'created', 'attach')
        read_only_fields = ('id', 'created')
        
    def create(self, validated_data):
        portfolio = Portfolio.objects.create(user=validated_data['user'], title=validated_data['title'], description=validated_data['description'], link=validated_data['link'])
        
        
                #att = Attach.objects.create(att=destination, portfolio=portfolio)
                #att.save()
        return portfolio


class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = ('user', 'f_name', 'l_name', 'bd_day', 'bd_month', 'bd_year', 'spec', 'company', 'rate', 'skills', 'bill_rate', 'website', 'about', 'city', 'avatar', 'filled')
        depth = 1

class ProfileUpdateSerializer(serializers.ModelSerializer):
    skills = serializers.PrimaryKeyRelatedField(many=True, queryset=Skills.objects.all(), required=False)
    
    class Meta:
        model = Profile
        fields = ('user', 'f_name', 'l_name', 'bd_day', 'bd_month', 'bd_year', 'spec', 'company', 'rate', 'skills', 'bill_rate', 'website', 'about', 'city', 'avatar', 'filled')
        
    def update(self, instance, validated_data):
        instance.user_id = validated_data.get('user', instance.user_id)
        instance.f_name = validated_data.get('f_name', instance.f_name)
        instance.l_name = validated_data.get('l_name', instance.l_name)
        instance.bd_day = validated_data.get('bd_day', instance.bd_day)
        instance.bd_month = validated_data.get('bd_month', instance.bd_month)
        instance.bd_year = validated_data.get('bd_year', instance.bd_year)
        instance.spec = validated_data.get('spec', instance.spec)
        instance.company = validated_data.get('company', instance.company)
        instance.rate = validated_data.get('rate', instance.rate)
        instance.website = validated_data.get('website', instance.website)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.about = validated_data.get('about', instance.about)
        instance.city = validated_data.get('city', instance.city)
        instance.filled = validated_data.get('filled', instance.filled)
        instance.skills = validated_data.get('skills')
        instance.save()
        return instance

class ProfileUpdateAvatarSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(max_length=None, use_url=True,)
    class Meta:
        model = Profile
        fields = ('avatar',)
        
    def update(self, instance, validated_data):
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return instance