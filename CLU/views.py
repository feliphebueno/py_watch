from django.shortcuts import render
from django.http import HttpResponse
from .models import Build

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def build_list(request):
    builds = Build.objects.all()
    return render(request, 'CLU/post_list.html', {'builds': builds})

def build(request, id):
    build = Build.objects.filter(buildCod=id)

    if(build.count() > 0):
        return render(request, 'CLU/build.html', {'build': build})
    else:
        return render(request, 'CLU/error.html', {})