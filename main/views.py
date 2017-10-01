from django.shortcuts import render
from django.template import Context, RequestContext

def error_404_page(request):
    return render(request, '404.html', {})

def error_401_page(request):
    return render(request, '401.html', {})

def error_50x_page(request):
    return render(request, '50x.html', {})

def index(request):
    context = {}
    return render(request, 'home.html', context)
