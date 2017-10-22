import pyknow
from main.djangoModels.fish.fishFeature import FishFeature
from main.pyknowEngines.fish import fishGlobals

class Features(pyknow.Fact):
    @classmethod
    def getNotFishFeatures(cls):
        ignoreFeatures = fishGlobals.request.POST.get('ignoreFeatures', '')
        newIgnoreFeatures = fishGlobals.request.POST.get('newIgnoreFeatures', '')
        if ignoreFeatures:
            ignoreFeatures = list(int(x) for x in ignoreFeatures.split('&'))
        else:
            ignoreFeatures = []
        if newIgnoreFeatures and 'feature_no' in fishGlobals.request.POST:
            newIgnoreFeatures = list(int(x) for x in newIgnoreFeatures.split('&'))
        else:
            newIgnoreFeatures = []
            
        ignoreFeatures = list(set().union(ignoreFeatures, newIgnoreFeatures))
        featuresList = []
        for feature in FishFeature.objects.all().exclude(id__in=ignoreFeatures):
            featuresList.append(pyknow.NOT(Features(feature=str(feature.id))))
        return featuresList if featuresList else [
            pyknow.Fact(action='featureNotDeclared')]
