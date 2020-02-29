from django.conf.urls import url
from django.urls import path
from post import views


urlpatterns = [
    path('ping', views.ping, name='ping'),
]
