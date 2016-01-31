from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.template import RequestContext

import os
ROOT_PATH = os.path.join(os.path.dirname(__file__), '..')
PORTFOLIO_DIR = os.path.abspath(ROOT_PATH)

from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser, FormParser, MultiPartParser, BaseParser
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404
from models import Profile, Portfolio, Skills, Attach
from serializers import ProfileSerializer, ProfileUpdateSerializer, ProfileUpdateAvatarSerializer, PortfolioSerializer, SkillsSerializer

class PlainTextParser(BaseParser):
    """
    Plain text parser.
    """
    media_type = 'text/plain'

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Simply return a string representing the body of the request.
        """
        return stream.read()

@login_required()
@api_view(['GET', 'PUT', 'PATCH'])
def profile(request, format=None):
    uid = request.user.id
    prof = Profile.objects.get(user_id=request.user)
    all_sk = Skills.objects.all()
    try:
        port = Portfolio.objects.filter(user=request.user.id)
    except:
        port = {}
    profile = ProfileSerializer(prof, many=False)
    portfolio = PortfolioSerializer(port, many=True)
    all_skills = SkillsSerializer(all_sk, many=True)
    context = {'profile': profile.data,
               'portfolio': portfolio.data,
               'all_skills': all_skills.data
               }
    if request.is_ajax():
        if request.method == 'GET':
            return Response(context)
        elif request.method == 'PUT':
            prof = Profile.objects.get(user_id=request.user)
            req_data = ProfileUpdateSerializer(prof, data=request.data, partial=True)
            if req_data.is_valid():
                req_data.save()
                prof = Profile.objects.get(user_id=request.user)
                profile = ProfileSerializer(prof)
                return Response(profile.data)
        elif request.method == 'PATCH':
            prof = Profile.objects.get(user_id=request.user)
            req_data = ProfileUpdateAvatarSerializer(prof, data=request.data, partial=True)
            if req_data.is_valid():
                req_data.save()
                prof = Profile.objects.get(user_id=request.user)
                profile = ProfileSerializer(prof)
                return Response(profile.data)
    return Response(template_name = 'profile.html')

class PortfolioCreate(APIView):
    parser_classes = (FormParser, MultiPartParser, PlainTextParser, )

    def post(self, request, format=None):
        uid = request.user.id
        req_data = PortfolioSerializer(data=request.data)
        if req_data.is_valid():
            p = req_data.save()
            for i in range(0,20):
                if request.data.get('file' + str(i)):
                    up_file = request.data.get('file' + str(i))
                    directory = PORTFOLIO_DIR + '/media/portfolios/' + request.user.username + '/'
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    destination = open(directory + up_file.name, 'wb+')
                    url = '/media/portfolios/' + request.user.username + '/' + up_file.name
                    for chunk in up_file.chunks():
                        destination.write(chunk)
                        destination.close()
                        att = Attach.objects.create(att=url, portfolio_id=p.id)
                        att.save()
            port = Portfolio.objects.filter(user=uid)
            portfolio = PortfolioSerializer(port, many=True)
            return Response(portfolio.data)
        return Response(template_name = 'profile.html')