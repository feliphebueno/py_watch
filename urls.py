from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    #url(r'^post/([0-9]{1,})/$', views.build),
]
