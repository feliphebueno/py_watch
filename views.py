from django.shortcuts import render

from stats.models import *


# Create your views here.
def index(request):
    return render(request, 'index.html', {})

def getUsers(request):
    users = User.objects.using('chat_watch').all()
    return render(request, 'users.html', {'users': users})

def userHistory(request, userId):
    history = Message.objects.using('chat_watch').filter(userid=userId)
    return render(request, 'userHistory.html', {'history': history})