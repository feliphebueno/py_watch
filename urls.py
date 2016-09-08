from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^users/?$', views.getUsers),
    url(r'^userHistory/([0-9]{1,})/?$', views.userHistory),
]
