from django.shortcuts import render
from django.template import Context, RequestContext
from django.views.decorators.cache import never_cache
from django.core.cache import cache
from main.labsViews.cache_decorator import never_ever_cache
from main.pyknowModels import fish

@never_cache
@never_ever_cache
def fishView(request):
    print("I am HERE") # BUG: NEED DISABLE CACHE
    fishEngine = fish.FishEngine()
    fishEngine.setRequest(request)
    fishEngine.reset()
    fishEngine.run()
    print("I am HERE") # BUG: NEED DISABLE CACHE
    if not hasattr(fishEngine, 'response'):
        fishEngine.getGraph()
        return render(request, 'labs/fish.html', {
            'facts': fishEngine.facts,
        })
    return fishEngine.response
