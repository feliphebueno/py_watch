from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^admin/', admin.site.urls),
    url(r'^users/?$', views.getUsers),
    url(r'^userHistory/([0-9]{1,})/?$', views.userHistory),
]
