
from django.shortcuts import render
from main.djangoModels.fish.fishFeature import FishFeature
from main.pyknowModels.fish.features import Features
from main.pyknowEngines.fish.baseEngine import BaseEngine
from main.pyknowEngines.fish import fishGlobals

import pyknow

class FeaturesEngine(BaseEngine):
    def declareFeatures(self, features):
        for feature in features:
            self.declare(Features(feature=feature))

    @pyknow.Rule(pyknow.Fact(action='consultationsFeature'),
            pyknow.OR(*Features.getNotFishFeatures()),
            salience=40)
    def askFeature(self, **kwargs):
        facts = [
            {'key': 'oldFeatures', 'fustyKey': 'feature',
                'button': '_submit',},
            {'key': 'idunnoFeatures', 'fustyKey': 'newIdunnoFeatures',
                'button': '_idunno',},
            {'key': 'ignoreFeatures', 'fustyKey': 'newIgnoreFeatures',
                'button': '_no',},
        ]
        isUpdated, fishGlobals.request = self.declareNewFacts(
            'feature', facts, fishGlobals.request)
        if isUpdated:
            return

        oldFeatures = fishGlobals.request.POST.get('oldFeatures', '')
        idunnoFeatures = fishGlobals.request.POST.get('idunnoFeatures', '')
        ignoreFeatures = fishGlobals.request.POST.get('ignoreFeatures', '')
        featuresList = []
        print('STEP2 idunnoFeatures:', idunnoFeatures, True if idunnoFeatures else False)
        ignoreFeatures = self.splitFactsString(ignoreFeatures)
        idunnoFeatures = self.splitFactsString(idunnoFeatures)
        print('STEP2 idunnoFeatures:', idunnoFeatures)

        for feature in FishFeature.objects.all().exclude(id__in=ignoreFeatures)\
                .exclude(id__in=idunnoFeatures):
            if str(feature.id) not in oldFeatures.split('&'):
                featuresList.append(feature)
        if not featuresList:
            for feature in FishFeature.objects.all().exclude(id__in=ignoreFeatures):
                featuresList.append(feature)
            self.changePostParametrs(fishGlobals.request, {
                'idunnoFeatures': '',
                'newIdunnoFeatures': '',
            }, [])

        featuresList = featuresList[0:5]
        if featuresList:
            newIdunnoFeatures, newIgnoreFeatures = self.getNewParams(featuresList)
            self.response = render(fishGlobals.request, 'labs/askFeature.html', {
                'question': 'Does the fish has one of the next features?',
                'features': featuresList,
                'newIdunnoFeatures': newIdunnoFeatures,
                'newIgnoreFeatures': newIgnoreFeatures,
                'answer_id': 'feature',
                'facts': self.facts,
                'url': '/bookExpert/fish', 
            })
        else:
            self.getGraph()
            return render(fishGlobals.request, 'labs/fish.html', {
                'facts': self.facts,
            })
