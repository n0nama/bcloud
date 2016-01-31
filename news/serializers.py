from rest_framework import serializers

from models import New, Comment, Reply, Attach
from users.models import Profile
from django.contrib.auth.models import User

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('f_name', 'l_name', 'avatar',)


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('username', 'profile',)


class AttachSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attach
        fields = ('att',)


class ReplySerializer(serializers.ModelSerializer):
    staff = UserSerializer()

    class Meta:
        model = Reply
        fields = ('id', 'staff', 'text', 'pub_date')


class CommentsSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    replies = ReplySerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'pub_date', 'replies')



class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('new', 'author', 'text', 'pub_date',)

    def update(self, instance, validated_data):
        instance.new = validated_data.get('new', instance.new)
        instance.author = validated_data.get('author', instance.author)
        instance.text = validated_data.get('text', instance.text)
        instance.pub_date = validated_data.get('pub_date', instance.pub_date)
        instance.save()
        return instance


class NewSerializer(serializers.ModelSerializer):
    attach = AttachSerializer(many=True, read_only=True)

    class Meta:
        model = New
        fields = ('id', 'title', 'text', 'status', 'marked', 'attach', 'pub_date', )

class NewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = New
        fields = ('id', 'title', 'text', 'status', 'marked', 'pub_date', )