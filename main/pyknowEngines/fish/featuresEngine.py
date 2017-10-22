
from django.shortcuts import render
from main.djangoModels.fish.fishFeature import FishFeature
from main.pyknowModels.fish.features import Features
from main.pyknowEngines.fish.baseEngine import BaseEngine
from main.pyknowEngines.fish import fishGlobals

import pyknow

class FeaturesEngine(BaseEngine):
    @pyknow.Rule(pyknow.Fact(action='consultationsFeature'),
            pyknow.OR(*Features.getNotFishFeatures()),
            salience=40)
    def askFeature(self, **kwargs):
        isUpdated, fishGlobals.request = self.declareNewFacts()
        if isUpdated:
            return

        oldFeatures = fishGlobals.request.POST.get('oldFeatures', '')
        idunnoFeatures = fishGlobals.request.POST.get('idunnoFeatures', '')
        ignoreFeatures = fishGlobals.request.POST.get('ignoreFeatures', '')
        featuresList = []
        oldFeatures = self.splitFactsString(oldFeatures)
        ignoreFeatures = self.splitFactsString(ignoreFeatures)
        idunnoFeatures = self.splitFactsString(idunnoFeatures)

        for feature in FishFeature.objects.all().exclude(id__in=ignoreFeatures)\
                .exclude(id__in=idunnoFeatures).exclude(id__in=oldFeatures):
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
