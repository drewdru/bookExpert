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
            facts, kindName = Kinds.from_django_model(kinds)
            print('-'*20)
            print(Features(features=pyknow.AND(*facts, cls('y' << pyknow.W())), 
                    kind=kindName << pyknow.W()))
            print('-'*20)
            # kindsList.append(Features(features=pyknow.AND(*facts), kind=kindName << pyknow.W()))
            kindsList.append(pyknow.AND(*facts))
            # kindsList.append('light' << pyknow.Fact(kindName))
                # cls(kind=kindName)))
        print(kindsList)
        return kindsList

    @classmethod
    def getNotFishKinds(cls, fishFeatures):
        kindsList = []
        for kinds in fishFeatures:
            kindsList.append(pyknow.NOT(pyknow.AND(
                *Kinds.from_django_model(kinds))))
        return kindsList