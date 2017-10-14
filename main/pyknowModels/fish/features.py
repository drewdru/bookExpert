import pyknow
from main.djangoModels.fish.fishFeature import FishFeature
from main.pyknowEngines.fish import fishGlobals
# from main.pyknowEngines.fish.fishGlobals import FishGlobals

class Features(pyknow.Fact):
    @classmethod
    def from_django_model(cls, obj):
        return cls(feature=str(obj.id))

    @classmethod
    def getNotFishFeatures(cls):
        ignoreFeatures = fishGlobals.request.POST.get('ignoreFeatures', '')
        newIgnoreList = fishGlobals.request.POST.get('newIgnoreList', '')
        if ignoreFeatures:
            ignoreFeatures = list(int(x) for x in ignoreFeatures.split('&'))
        else:
            ignoreFeatures = []
        if newIgnoreList and '_no' in fishGlobals.request.POST:
            newIgnoreList = list(int(x) for x in newIgnoreList.split('&'))
        else:
            newIgnoreList = []
            
        ignoreFeatures = list(set().union(ignoreFeatures, newIgnoreList))
        featuresList = []
        for feature in FishFeature.objects.all().exclude(id__in=ignoreFeatures):
            featuresList.append(pyknow.NOT(Features.from_django_model(feature)))
        return featuresList if featuresList else [
            pyknow.Fact(action='notDeclared')]

    # @classmethod
    # def getIgnoreFeatures(cls, request):
    #     ignoreFeatures = request.POST.get('ignoreFeatures', '')
    #     featuresList = []
    #     for feature in ignoreFeatures.split('&'):
    #         featuresList.append(pyknow.NOT(cls(feature=feature)))
    #     return featuresList

    # @classmethod
    # def getFishFeatures(cls):
    #     featuresList = []
    #     for feature in FishFeature.objects.all():
    #         featuresList.append(Features.from_django_model(feature))
    #     return featuresList

