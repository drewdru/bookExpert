from django.shortcuts import render
from django.template import Context, RequestContext
from django.views.decorators.cache import never_cache
from django.core.cache import cache
from main.labsViews.cache_decorator import never_ever_cache
from main.pyknowEngines.fish import fishEngine

@never_cache
@never_ever_cache
def fishView(request):
    fishEng = fishEngine.FishEngine()
    fishEngine.MODULE_REQUEST = request
    fishEng.reset()
    fishEng.run()
    if not hasattr(fishEng, 'response'):
        fishEng.getGraph()
        return render(request, 'labs/fish.html', {
            'facts': fishEng.facts,
        })
    return fishEng.response
