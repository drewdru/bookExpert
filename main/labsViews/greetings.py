from main.pyknowModels import greetings
from django.shortcuts import render
from django.template import Context, RequestContext
from django.views.decorators.cache import never_cache
from django.core.cache import cache
from main.labsViews.cache_decorator import never_ever_cache

@never_cache
@never_ever_cache
def greetingsView(request):
    print("I am HERE") # BUG: NEED DISABLE CACHE
    greetingsEngine = greetings.Greetings()
    greetingsEngine.setRequest(request)
    greetingsEngine.reset()
    greetingsEngine.run()
    print("I am HERE") # BUG: NEED DISABLE CACHE
    return greetingsEngine.response
