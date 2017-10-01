# -*- coding: utf-8 -*-
from django import template
register = template.Library()

@register.filter
def getParameters(request):
    params_list = []
    for key, value in request.GET.items():
        params_list.append({'key': key, 'value': value})
    return params_list

@register.filter
def postParameters(request):
    params_list = []
    for key, value in request.POST.items():
        params_list.append({'key': key, 'value': value})
    return params_list