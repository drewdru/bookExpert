
from django.shortcuts import render
from main.djangoModels.fish.fishKind import FishKind
from main.pyknowModels.fish.kinds import Kinds
from main.pyknowEngines.fish.baseEngine import BaseEngine

import pyknow
import random
from main.pyknowEngines.fish import fishGlobals

class KindsEngine(BaseEngine):
    def declareKinds(self, kinds):
        for kind in kinds:
            self.declare(Kinds(kind=kind))

    @pyknow.Rule(pyknow.Fact(action='consultationsKind'),
            pyknow.OR(*Kinds.getNotFishKinds()),
            salience=40)
    def askKind(self, **kwargs):
        facts = [
            {'key': 'oldFeatures', 'fustyKey': 'feature',
                'button': 'feature_submit',},
            {'key': 'idunnoFeatures', 'fustyKey': 'newIdunnoFeatures',
                'button': 'feature_idunno',},
            {'key': 'ignoreFeatures', 'fustyKey': 'newIgnoreFeatures',
                'button': 'feature_no',},
            {'key': 'oldKinds', 'fustyKey': 'kind',
                'button': 'kind_submit',},
            {'key': 'idunnoKinds', 'fustyKey': 'newIdunnoKinds',
                'button': 'kind_idunno',},
            {'key': 'ignoreKinds', 'fustyKey': 'newIgnoreKinds',
                'button': 'kind_no',},
        ]
        isUpdated, fishGlobals.request = self.declareNewFacts(
            'kind', facts, fishGlobals.request)
        if isUpdated:
            return

        oldKinds = fishGlobals.request.POST.get('oldKinds', '')
        idunnoKinds = fishGlobals.request.POST.get('idunnoKinds', '')
        ignoreKinds = fishGlobals.request.POST.get('ignoreKinds', '')
        kindsList = []
        oldKinds = self.splitFactsString(oldKinds)
        ignoreKinds = self.splitFactsString(ignoreKinds)
        idunnoKinds = self.splitFactsString(idunnoKinds)

        for kind in FishKind.objects.all().exclude(id__in=ignoreKinds)\
                .exclude(id__in=idunnoKinds).exclude(id__in=oldKinds):
            kindsList.append(kind)
        if not kindsList:
            for kind in FishKind.objects.all().exclude(id__in=ignoreKinds):
                kindsList.append(kind)
            self.changePostParametrs(fishGlobals.request, {
                'idunnoKinds': '',
                'newIdunnoKinds': '',
            }, [])

        kindsList = kindsList[0:5]
        if kindsList:
            newIdunnoKinds, newIgnoreKinds = self.getNewParams(kindsList)
            self.response = render(fishGlobals.request, 'labs/askKind.html', {
                'question': 'Does the fish has one of the next kinds?',
                'kinds': kindsList,
                'newIdunnoKinds': newIdunnoKinds,
                'newIgnoreKinds': newIgnoreKinds,
                'answer_id': 'kind',
                'facts': self.facts,
                'url': '/bookExpert/fish', 
            })
        else:
            self.getGraph()
            return render(fishGlobals.request, 'labs/fish.html', {
                'facts': self.facts,
            })
    




    def declareKindsObjects(self, kinds):
        for kind in kinds:
            self.declare(Kinds(kind=kind.id))

    @pyknow.Rule(pyknow.NOT(pyknow.Fact(action='answerKind')),
            pyknow.OR(*Kinds.getKindsFeatures()),
            salience=30)
    def declareKindByFeature(self, kwargs):
        featureList = []
        for key, value in kwargs.items():
            if key.startswith('feature_'):
                featureList.append(int(value['feature']))
        kinds = FishKind.objects.all().filter(features__in=featureList)
        self.declareKindsObjects(kinds)


    @pyknow.Rule(pyknow.Fact(action='answerKind'),
            pyknow.OR(*Kinds.getKindsFeatures()),
            salience=30)
    def answerKind(self, **kwargs):
        featureList = []
        for key, value in kwargs.items():
            if key.startswith('feature_'):
                featureList.append(int(value['feature']))
        kinds = FishKind.objects.all().filter(features__in=featureList)
        kind = random.choice(kinds)
        self.getGraph()
        self.response = render(fishGlobals.request, 'labs/fish.html', {
            'answer': kind.kind,
            'facts': self.facts,
            'url': '/bookExpert/fish', 
        })
