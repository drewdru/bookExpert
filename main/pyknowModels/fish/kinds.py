from .features import Features
from main.djangoModels.fish.fishKind import FishKind
from main.pyknowEngines.fish import fishGlobals

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

    @classmethod
    def getNotFishKinds(cls):
        ignoreKinds = fishGlobals.request.POST.get('ignoreKinds', '')
        newIgnoreKinds = fishGlobals.request.POST.get('newIgnoreKinds', '')
        if ignoreKinds:
            ignoreKinds = list(int(x) for x in ignoreKinds.split('&'))
        else:
            ignoreKinds = []
        if newIgnoreKinds and 'kind_no' in fishGlobals.request.POST:
            newIgnoreKinds = list(int(x) for x in newIgnoreKinds.split('&'))
        else:
            newIgnoreKinds = []
            
        ignoreKinds = list(set().union(ignoreKinds, newIgnoreKinds))
        kindsList = []
        for kind in FishKind.objects.all().exclude(id__in=ignoreKinds):
            kindsList.append(pyknow.NOT(Kinds(kind=str(kind.id))))
        return kindsList if kindsList else [pyknow.Fact(action='kindNotDeclared')]
