
from django.shortcuts import render
from main.djangoModels.fish.fishDetachment import FishDetachment
from main.pyknowModels.fish.detachments import Detachments
from main.pyknowEngines.fish.baseEngine import BaseEngine

import pyknow
import random
from main.pyknowEngines.fish import fishGlobals

class DetachmentsEngine(BaseEngine):
    def declareDetachments(self, detachments):
        for detachment in detachments:
            self.declare(Detachments(detachment=detachment))

    @pyknow.Rule(pyknow.Fact(action='consultationsDetachment'),
            pyknow.OR(*Detachments.getNotFishDetachments()),
            salience=40)
    def askDetachment(self, **kwargs):
        facts = [
            {'key': 'oldDetachments', 'fustyKey': 'detachment',
                'button': '_submit',},
            {'key': 'idunnoDetachments', 'fustyKey': 'newIdunnoDetachments',
                'button': '_idunno',},
            {'key': 'ignoreDetachments', 'fustyKey': 'newIgnoreDetachments',
                'button': '_no',},
        ]
        isUpdated, fishGlobals.request = self.declareNewFacts(
            'detachment', facts, fishGlobals.request)
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
            newIdunnoDetachments, newIgnoreDetachments = self.getNewParams(DetachmentsList)
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
    def declareDetachmentByFeature(self, kwargs):
        featureList = []
        for key, value in kwargs.items():
            if key.startswith('feature_'):
                featureList.append(int(value['feature']))
        detachments = FishDetachment.objects.all().filter(features__in=featureList)
        self.declareDetachmentsObjects(Detachments)


    @pyknow.Rule(pyknow.Fact(action='answerDetachment'),
            pyknow.OR(*Detachments.getDetachmentsFacts()),
            salience=30)
    def answerDetachment(self, **kwargs):
        featureList = []
        for key, value in kwargs.items():
            if key.startswith('feature_'):
                featureList.append(int(value['feature']))
        detachments = FishDetachment.objects.all().filter(features__in=featureList)
        detachment = random.choice(detachments)
        self.getGraph()
        self.response = render(fishGlobals.request, 'labs/fish.html', {
            'answer': detachment.detachment,
            'facts': self.facts,
            'url': '/bookExpert/fish', 
        })
