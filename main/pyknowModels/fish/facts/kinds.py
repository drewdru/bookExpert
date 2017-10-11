from .features import Features

import pyknow

class Kinds(pyknow.Fact):
    @classmethod
    def from_django_model(cls, obj):
        facts = []
        for feature in obj.features.all():
            facts.append(Features(feature=feature.feature))
        # facts.append(cls(kind=obj.kind))
        return facts

    @classmethod
    def getIgnoreKinds(cls, request, fishFeatures):
        ignoreKinds = request.POST.get('ignoreKinds', '')
        kindsList = []
        for kind in ignoreKinds.split('&'):
            for kinds in fishFeatures.filter(kind=kind):
                kindsList.append(pyknow.AND(*Kinds.from_django_model(kinds)))
        return kindsList if kindsList else [pyknow.Fact()]

    @classmethod
    def getFishKinds(cls, fishFeatures):
        kindsList = []
        for kinds in fishFeatures:
            kindsList.append(pyknow.AND(*Kinds.from_django_model(kinds)))
        print(kindsList)
        return kindsList

    @classmethod
    def getNotFishKinds(cls, fishFeatures):
        kindsList = []
        for kinds in fishFeatures:
            kindsList.append(pyknow.NOT(pyknow.AND(
                *Kinds.from_django_model(kinds))))
        return kindsList