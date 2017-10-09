from django.shortcuts import render
from django.template import Context, RequestContext
from django.views.decorators.cache import never_cache
from django.core.cache import cache
from main.labsViews.cache_decorator import never_ever_cache
from main.pyknowModels.fish import fishEngine

@never_cache
@never_ever_cache
def fishView(request):
    ignoreFeatures = request.POST.get('ignoreFeatures', '')
    print('fishView ignoreFeatures:', ignoreFeatures)
    fishEng = fishEngine.FishEngine()
    fishEngine.MODULE_REQUEST = request
    # fishEng.initPost()
    fishEng.reset()
    fishEng.run()
    if not hasattr(fishEng, 'response'):
        fishEng.getGraph()
        return render(request, 'labs/fish.html', {
            'facts': fishEng.facts,
        })
    return fishEng.response

# if not hasattr(fishEng, 'response'):
#         fishEng.getGraph()
#         facts = fishEng.facts
#         del fishEng
#         return render(request, 'labs/fish.html', {
#             'facts': facts,
#         })
#     response = fishEng.response
#     del fishEng
#     return response
