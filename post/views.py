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

    def create(self, request, *args, **kwargs):
        try:
            payload = request.data.copy()
            serializer = self.get_serializer(data=payload)
            serializer.is_valid(raise_exception=True)
            resp = Post.objects.create(**serializer.validated_data)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED, headers=headers)

        except Exception:
            logger.error(traceback.format_exc())
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
