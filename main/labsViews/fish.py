from django.shortcuts import render
from django.template import Context, RequestContext

# # singleton START
# from main.pyknowEngines.fish.fishGlobals import FishGlobals
# from main.pyknowEngines.fish import fishEngine
# from main.pyknowEngines.fish import featuresEngine
# from main.pyknowEngines.fish import kindsEngine
# from main.pyknowModels.fish import features
# from main.pyknowModels.fish import kinds
# # singleton END
from main.pyknowEngines.fish import fishGlobals


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
