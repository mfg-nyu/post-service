from django.conf.urls import include, url
from django.urls import path
from post import views

from rest_framework_mongoengine import routers

router = routers.DefaultRouter()
router.register(r'', views.PostViewSet, basename='')

urlpatterns = [
    path('ping', views.ping, name='ping'),
    url(r'^', include(router.urls)),
]
