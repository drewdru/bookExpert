
from django.shortcuts import render
from main.djangoModels.fish.fishFeature import FishFeature
from main.pyknowModels.fish.features import Features
from main.pyknowEngines.fish.baseEngine import BaseEngine

import pyknow

class FeaturesEngine(BaseEngine):
    def declareFeatures(self, features):
        for feature in features:
            self.declare(Features(feature=feature))

    @pyknow.Rule(pyknow.Fact(action='consultationsFeature'),
            pyknow.OR(*Features.getNotFishFeatures()),
            salience=40)
            # pyknow.AND(*Features.getIgnoreFeatures(MODULE_REQUEST)),
            # pyknow.OR(*Features.getNotFishFeatures(FISH_FEATURES)))
    def askFeature(self, **kwargs):
        newFeature = FeaturesEngine.request.POST.get('feature', '')
        oldFeatures = FeaturesEngine.request.POST.get('oldFeatures', '')
        ignoreFeatures = FeaturesEngine.request.POST.get('ignoreFeatures', '')
        print(ignoreFeatures)
        if newFeature != '':
            if oldFeatures == '' and '!feature!' not in newFeature:
                oldFeatures = newFeature
            elif '!feature!' not in newFeature:
                oldFeatures += '&{}'.format(newFeature)
            if '!feature!'in newFeature:
                ignore = newFeature.replace('!feature!', '')
                if ignoreFeatures == '':
                    ignoreFeatures = ignore
                else:
                    ignoreFeatures += '&{}'.format(ignore)
            self.changePostParametrs(FeaturesEngine.request, {
                    'oldFeatures': oldFeatures,
                    'ignoreFeatures': ignoreFeatures
                }, ['feature'])
            self.declareFeatures(oldFeatures.split('&'))
            return

        featuresList = []
        for feature in FishFeature.objects.all():
            if str(feature.id) not in oldFeatures.split('&') and\
                    str(feature.id) not in ignoreFeatures.split('&'):
                featuresList.append(feature)
        # featuresList = featuresList[0:5]
        featuresToIgnore = ''
        for feature in featuresList:
            if featuresToIgnore == '':
                featuresToIgnore = '{}'.format(feature)
            else:
                featuresToIgnore += '&{}'.format(feature)

        self.response = render(FeaturesEngine.request, 'labs/askFeature.html', {
            'question': 'Does the fish has one of the next features?',
            'features': featuresList,
            'featuresToIgnore': featuresToIgnore,
            'answer_id': 'feature',
            'facts': self.facts,
            'url': '/bookExpert/fish', 
        })
