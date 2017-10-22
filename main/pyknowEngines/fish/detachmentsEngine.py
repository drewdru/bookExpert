
from django.shortcuts import render
from main.djangoModels.fish.fishDetachment import FishDetachment
from main.pyknowModels.fish.detachments import Detachments
from main.pyknowEngines.fish.baseEngine import BaseEngine

import pyknow
import random
from main.pyknowEngines.fish import fishGlobals

class DetachmentsEngine(BaseEngine):
    @pyknow.Rule(pyknow.Fact(action='consultationsDetachment'),
            pyknow.OR(*Detachments.getNotFishDetachments()),
            salience=40)
    def askDetachment(self, **kwargs):
        isUpdated, fishGlobals.request = self.declareNewFacts()
        if isUpdated:
            return

        oldDetachments = fishGlobals.request.POST.get('oldDetachments', '')
        idunnoDetachments = fishGlobals.request.POST.get('idunnoDetachments', '')
        ignoreDetachments = fishGlobals.request.POST.get('ignoreDetachments', '')
        detachmentsList = []
        oldDetachments = self.splitFactsString(oldDetachments)
        ignoreDetachments = self.splitFactsString(ignoreDetachments)
        idunnoDetachments = self.splitFactsString(idunnoDetachments)

        for detachment in FishDetachment.objects.all().exclude(id__in=ignoreDetachments)\
                .exclude(id__in=idunnoDetachments).exclude(id__in=oldDetachments):
            detachmentsList.append(detachment)
        if not detachmentsList:
            for detachment in FishDetachment.objects.all().exclude(id__in=ignoreDetachments):
                detachmentsList.append(detachment)
            self.changePostParametrs(fishGlobals.request, {
                'idunnoDetachments': '',
                'newIdunnoDetachments': '',
            }, [])

        detachmentsList = detachmentsList[0:5]
        if detachmentsList:
            newIdunnoDetachments, newIgnoreDetachments = self.getNewParams(detachmentsList)
            self.response = render(fishGlobals.request, 'labs/askDetachment.html', {
                'question': 'Does the fish has one of the next detachments?',
                'detachments': detachmentsList,
                'newIdunnoDetachments': newIdunnoDetachments,
                'newIgnoreDetachments': newIgnoreDetachments,
                'answer_id': 'detachment',
                'facts': self.facts,
                'url': '/bookExpert/fish', 
            })
        else:
            self.getGraph()
            return render(fishGlobals.request, 'labs/fish.html', {
                'facts': self.facts,
            })
    




    def declareDetachmentsObjects(self, detachments):
        for detachment in detachments:
            self.declare(Detachments(detachment=detachment.id))

    @pyknow.Rule(pyknow.NOT(pyknow.Fact(action='answerDetachment')),
            pyknow.OR(*Detachments.getDetachmentsFacts()),
            salience=30)
    def declareDetachmentByFeature(self, **kwargs):
        featureList = self.getFeatureList(kwargs, 'feature')
        kindList = self.getFeatureList(kwargs, 'kind')
        if featureList and kindList
            detachments = FishDetachment.objects.all().filter(
                features__in=featureList).filter(kinds__in=kindList)
            self.declareDetachmentsObjects(detachments)



    def getFeatureList(self, kwargs, prefix):
        featureList = []
        for key, value in kwargs.items():
            if key.startswith('{}_'.format(prefix)):
                featureList.append(int(value[prefix]))

    @pyknow.Rule(pyknow.Fact(action='answerDetachment'),
            pyknow.OR(*Detachments.getDetachmentsFacts()),
            salience=30)
    def answerDetachment(self, **kwargs):
        featureList = self.getFeatureList(kwargs, 'feature')
        kindList = self.getFeatureList(kwargs, 'kind')
        detachments = FishDetachment.objects.all().filter(
            features__in=featureList).filter(kinds__in=kindList)
        detachment = random.choice(detachments)
        self.getGraph()
        self.response = render(fishGlobals.request, 'labs/fish.html', {
            'answer': detachment.detachment,
            'facts': self.facts,
            'url': '/bookExpert/fish', 
        })
