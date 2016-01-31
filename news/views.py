# coding=utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.template import RequestContext

from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from models import New, Comment
from serializers import NewSerializer, NewsSerializer, CommentSerializer, CommentsSerializer

@login_required()
@api_view(['GET'])
def news_list(request, format=None):
    news = New.objects.all().order_by('-pub_date')
    serializer = NewsSerializer(news, many=True)
    if request.is_ajax():
        return Response(serializer.data)
    return Response(template_name = 'news.html')

@login_required()
@api_view(['GET', 'POST', 'UPDATE', 'DELETE'])
def single_new(request, new_id, format=None):
    new = New.objects.filter(pk=new_id)
    comments = Comment.objects.filter(new=new_id)
    response = NewSerializer(new, many=True)
    rescom = CommentsSerializer(comments, many=True)
    content = {
        'user': unicode(request.user),
        'uid': request.user.id,
        'post': response.data,
        'comments': rescom.data,
    }
    if request.is_ajax():
        if request.method == 'GET':
            return Response(content)
        elif request.method == 'POST':
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                comments = Comment.objects.filter(new=new_id)
                rescom = CommentsSerializer(comments, many=True)
                return Response(rescom.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'UPDATE':
            cid = int(request.data['pk'])
            comment = Comment.objects.get(id=cid)
            serializer = CommentSerializer(instance=comment, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                comments = Comment.objects.filter(new=new_id)
                rescom = CommentsSerializer(comments, many=True)
                return Response(rescom.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            cid = int(request.data['pk'])
            comment = Comment.objects.filter(id=cid)
            comment.delete()
            comments = Comment.objects.filter(new=new_id)
            rescom = CommentsSerializer(comments, many=True)
            return Response(rescom.data)
    return Response(template_name = 'news.html')