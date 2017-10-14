from .features import Features
from main.djangoModels.fish.fishKind import FishKind

import pyknow

class Kinds(pyknow.Fact):
    @classmethod
    def from_django_model(cls, obj):
        facts = []
        for indx, feature in enumerate(obj.features.all()):
            facts.append('feature_{}'.format(indx) << Features(
                feature=str(feature.id)))
        return facts, obj.kind

    @classmethod
    def getKindsFeatures(cls):
        kindsList = []
        for kinds in FishKind.objects.all():
            facts, kindName = Kinds.from_django_model(kinds)
            kindsList.append(pyknow.AND(*facts))
        return kindsList

    # @classmethod
    # def getNotFishKinds(cls):
    #     kindsList = []
    #     for kinds in FishKind.objects.all():
    #         kindsList.append(pyknow.NOT(pyknow.AND(
    #             *Kinds.from_django_model(kinds))))
    #     return kindsList if kindsList else [pyknow.Fact(action='notDeclared')]

    # @classmethod
    # def getIgnoreKindsFeatures(cls, request):
    #     ignoreKinds = request.POST.get('ignoreKinds', '')
    #     kindsList = []
    #     for kind in ignoreKinds.split('&'):
    #         for kinds in FishKind.objects.all().filter(kind=kind):
    #             kindsList.append(pyknow.AND(*Kinds.from_django_model(kinds)))
    #     return kindsList if kindsList else [pyknow.Fact(action='notDeclared')]

