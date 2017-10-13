from .features import Features

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
    def getIgnoreKindsFeatures(cls, request, fishFeatures):
        ignoreKinds = request.POST.get('ignoreKinds', '')
        kindsList = []
        for kind in ignoreKinds.split('&'):
            for kinds in fishFeatures.filter(kind=kind):
                kindsList.append(pyknow.AND(*Kinds.from_django_model(kinds)))
        return kindsList if kindsList else [pyknow.Fact()]

    @classmethod
    def getKindsFeatures(cls, fishFeatures):
        kindsList = []
        for kinds in fishFeatures:
            facts, kindName = Kinds.from_django_model(kinds)
            kindsList.append(pyknow.AND(*facts))
        return kindsList

    @classmethod
    def getNotFishKinds(cls, fishFeatures):
        kindsList = []
        for kinds in fishFeatures:
            kindsList.append(pyknow.NOT(pyknow.AND(
                *Kinds.from_django_model(kinds))))
        return kindsList