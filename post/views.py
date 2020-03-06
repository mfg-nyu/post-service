import logging
import traceback

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import mixins, status, views
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets

from post.models import Post
from post.serializers import PostSerializer

logger = logging.getLogger(__name__)


def ping(request):
    return HttpResponse('Pong')


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.order_by('-created')
    serializer_class = PostSerializer
