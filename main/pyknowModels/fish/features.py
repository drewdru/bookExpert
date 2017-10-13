import pyknow
from main.djangoModels.fish.fishFeature import FishFeature

class Features(pyknow.Fact):
    @classmethod
    def from_django_model(cls, obj):
        return cls(feature=str(obj.id))

    @classmethod
    def getIgnoreFeatures(cls, request):
        ignoreFeatures = request.POST.get('ignoreFeatures', '')
        featuresList = []
        for feature in ignoreFeatures.split('&'):
            featuresList.append(pyknow.NOT(cls(feature=feature)))
        return featuresList

    @classmethod
    def getFishFeatures(cls):
        featuresList = []
        for feature in FishFeature.objects.all():
            featuresList.append(Features.from_django_model(feature))
        return featuresList

    @classmethod
    def getNotFishFeatures(cls):
        featuresList = []
        for feature in FishFeature.objects.all():
            featuresList.append(pyknow.NOT(
                Features.from_django_model(feature)))
        return featuresList
