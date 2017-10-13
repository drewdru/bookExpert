from django.shortcuts import render
from django.template import Context, RequestContext
from main.pyknowEngines.fish import fishEngine

def fishView(request):
    fishEng = fishEngine.FishEngine()
    fishEng.initRequest(request)
    fishEng.reset()
    fishEng.run()
    if not hasattr(fishEng, 'response'):
        fishEng.getGraph()
        return render(request, 'labs/fish.html', {
            'facts': fishEng.facts,
        })
    return fishEng.response
