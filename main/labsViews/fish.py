from django.shortcuts import render
from django.template import Context, RequestContext

from main.pyknowEngines.fish import fishGlobals

from django.views.decorators.cache import never_cache

@never_cache
def fishView(request):
    fishGlobals.request = request
    from main.pyknowEngines.fish.fishEngine import FishEngine # fix: import exec
    fishEng = FishEngine()
    fishEng.reset()
    fishEng.run()
    if not hasattr(fishEng, 'response'):
        fishEng.getGraph()
        return render(request, 'labs/fish.html', {
            'facts': fishEng.facts,
        })
    return fishEng.response
