from .features import Features
from main.djangoModels.fish.fishKind import FishKind

import pyknow

class Kinds(pyknow.Fact):
    @classmethod
    def featuresFromModel(cls, obj):
        facts = []
        for indx, feature in enumerate(obj.features.all()):
            facts.append('feature_{}'.format(indx) << Features(
                feature=str(feature.id)))
        return facts

    @classmethod
    def getKindsFeatures(cls):
        kindsList = []
        for kinds in FishKind.objects.all():
            facts = Kinds.featuresFromModel(kinds)
            kindsList.append(pyknow.AND(*facts))
        return kindsList
