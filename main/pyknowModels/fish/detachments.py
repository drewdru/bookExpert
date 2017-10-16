from .features import Features
from .kinds import Kinds
from main.djangoModels.fish.fishDetachment import FishDetachment
from main.pyknowEngines.fish import fishGlobals

import pyknow

class Detachments(pyknow.Fact):
    @classmethod
    def factsFromModel(cls, obj):
        facts = []
        kinds = []
        for indx, feature in enumerate(obj.features.all()):
            facts.append('feature_{}'.format(indx) << Features(
                feature=str(feature.id)))
        for indx, kind in enumerate(obj.kinds.all()):
            facts.append('kind_{}'.format(indx) << Kinds(
                kind=str(kind.id)))
        return facts, kinds

    @classmethod
    def getDetachmentsFacts(cls):
        kindsList = []
        for detachments in FishDetachment.objects.all():
            facts, kinds = Detachments.factsFromModel(detachments)
            kindsList.append(pyknow.OR(pyknow.AND(*facts), pyknow.AND(*facts)))
        return kindsList

    @classmethod
    def getNotFishDetachments(cls):
        ignoreDetachments = fishGlobals.request.POST.get('ignoreDetachments', '')
        newIgnoreDetachments = fishGlobals.request.POST.get('newIgnoreDetachments', '')
        if ignoreDetachments:
            ignoreDetachments = list(int(x) for x in ignoreDetachments.split('&'))
        else:
            ignoreDetachments = []
        if newIgnoreDetachments and '_no' in fishGlobals.request.POST:
            newIgnoreDetachments = list(int(x) for x in newIgnoreDetachments.split('&'))
        else:
            newIgnoreDetachments = []
            
        ignoreDetachments = list(set().union(ignoreDetachments, newIgnoreDetachments))
        detachmentsList = []
        for detachment in FishDetachment.objects.all().exclude(id__in=ignoreDetachments):
            detachmentsList.append(pyknow.NOT(Detachments(detachment=str(detachment.id))))
        return detachmentsList if detachmentsList else [
            pyknow.Fact(action='notDeclared')]
