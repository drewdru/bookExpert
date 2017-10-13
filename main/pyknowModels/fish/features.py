import pyknow

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
    def getFishFeatures(cls, fishFeatures):
        featuresList = []
        for feature in fishFeatures:
            featuresList.append(Features.from_django_model(feature))
        return featuresList

    @classmethod
    def getNotFishFeatures(cls, fishFeatures):
        featuresList = []
        for feature in fishFeatures:
            featuresList.append(pyknow.NOT(
                Features.from_django_model(feature)))
        return featuresList
