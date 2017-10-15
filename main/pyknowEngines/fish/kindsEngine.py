
from django.shortcuts import render
from main.djangoModels.fish.fishKind import FishKind
from main.pyknowModels.fish.kinds import Kinds
from main.pyknowEngines.fish.baseEngine import BaseEngine

import pyknow
import random
from main.pyknowEngines.fish import fishGlobals

class KindsEngine(BaseEngine):
    # def declareKinds(self, kinds):
    #     for kind in kinds:
    #         self.declare(Kinds(kind=kind))

    # def updateParametr(self, buttonName, oldValue, newValue):
    #     if oldValue == '' and buttonName in fishGlobals.request.POST:
    #         oldValue = newValue
    #     elif buttonName in fishGlobals.request.POST:
    #         oldValue += '&{}'.format(newValue)
    #     return oldValue

    # def declareNewKinds(self):
    #     oldKinds = fishGlobals.request.POST.get('oldKinds', '')
    #     newKind = fishGlobals.request.POST.get('kind', '')
    #     idunnoKinds = fishGlobals.request.POST.get('idunnoKinds', '')
    #     newIdunnoKinds = fishGlobals.request.POST.get('newIdunnoKinds', '')
    #     ignoreKinds = fishGlobals.request.POST.get('ignoreKinds', '')
    #     newIgnoreKinds = fishGlobals.request.POST.get('newIgnoreKinds', '')
    #     if newKind != '':
    #         oldKinds = self.updateParametr('_submit', oldKinds,
    #             newKind, fishGlobals.request)
    #         idunnoKinds = self.updateParametr('_idunno', idunnoKinds,
    #             newIdunnoKinds, fishGlobals.request)
    #         ignoreKinds = self.updateParametr('_no', ignoreKinds,
    #             newIgnoreKinds, fishGlobals.request)
    #         self.changePostParametrs(fishGlobals.request, {
    #             'oldKinds': oldKinds,
    #             'idunnoKinds': idunnoKinds,
    #             'ignoreKinds': ignoreKinds,
    #         }, [
    #             'Kind',
    #             'newIdunnoKinds',
    #             'newIgnoreKinds',
    #             '_submit',
    #             '_idunno',
    #             '_no',
    #         ])
    #         if oldKinds != '':
    #             self.declareKinds(oldKinds.split('&'))
    #         return True
    #     return False

    # @pyknow.Rule(pyknow.Fact(action='consultationsFeature'),
    #         pyknow.OR(*Features.getNotFishFeatures()),
    #         salience=40)
    # def askFeature(self, **kwargs):
    #     if self.declareNewFeatures():
    #         return

    #     oldFeatures = fishGlobals.request.POST.get('oldFeatures', '')
    #     idunnoFeatures = fishGlobals.request.POST.get('idunnoFeatures', '')
    #     ignoreFeatures = fishGlobals.request.POST.get('ignoreFeatures', '')
    #     featuresList = []
    #     ignoreFeatures = self.splitFactsString(ignoreFeatures)
    #     idunnoFeatures = self.splitFactsString(idunnoFeatures)

    #     for feature in FishFeature.objects.all().exclude(id__in=ignoreFeatures)\
    #             .exclude(id__in=idunnoFeatures):
    #         if str(feature.id) not in oldFeatures.split('&'):
    #             featuresList.append(feature)
    #     if not featuresList:
    #         for feature in FishFeature.objects.all().exclude(id__in=ignoreFeatures):
    #             featuresList.append(feature)
    #         self.changePostParametrs(fishGlobals.request, {
    #             'idunnoFeatures': '',
    #             'newIdunnoFeatures': '',
    #         }, [])

    #     featuresList = featuresList[0:5]
    #     if featuresList:
    #         newIdunnoFeatures, newIgnoreFeatures = self.getNewParams(featuresList)
    #         self.response = render(fishGlobals.request, 'labs/askFeature.html', {
    #             'question': 'Does the fish has one of the next features?',
    #             'features': featuresList,
    #             'newIdunnoFeatures': newIdunnoFeatures,
    #             'newIgnoreFeatures': newIgnoreFeatures,
    #             'answer_id': 'feature',
    #             'facts': self.facts,
    #             'url': '/bookExpert/fish', 
    #         })
    #     else:
    #         self.getGraph()
    #         return render(fishGlobals.request, 'labs/fish.html', {
    #             'facts': self.facts,
    #         })
    




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
            'amswer': kind.kind,
            'facts': self.facts,
            'url': '/bookExpert/fish', 
        })
