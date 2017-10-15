
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

    def updateParametr(self, buttonName, oldValue, newValue):
        if oldValue == '' and buttonName in fishGlobals.request.POST:
            oldValue = newValue
        elif buttonName in fishGlobals.request.POST:
            oldValue += '&{}'.format(newValue)
        return oldValue

    def declareNewFeatures(self):
        oldFeatures = fishGlobals.request.POST.get('oldFeatures', '')
        newFeature = fishGlobals.request.POST.get('feature', '')

        idunnoFeatures = fishGlobals.request.POST.get('idunnoFeatures', '')
        newIdunnoFeatures = fishGlobals.request.POST.get('newIdunnoFeatures', '')
        
        ignoreFeatures = fishGlobals.request.POST.get('ignoreFeatures', '')
        newIgnoreFeatures = fishGlobals.request.POST.get('newIgnoreFeatures', '')

        if newFeature != '':
            oldFeatures = self.updateParametr('_submit', oldFeatures, newFeature)
            idunnoFeatures = self.updateParametr('_idunno', idunnoFeatures, newIdunnoFeatures)
            ignoreFeatures = self.updateParametr('_no', ignoreFeatures, newIgnoreFeatures)
            self.changePostParametrs(fishGlobals.request, {
                'oldFeatures': oldFeatures,
                'idunnoFeatures': idunnoFeatures,
                'ignoreFeatures': ignoreFeatures,
            }, [
                'feature',
                'newIdunnoFeatures',
                'newIgnoreFeatures',
                '_submit',
                '_idunno',
                '_no',
            ])
            if oldFeatures != '':
                self.declareFeatures(oldFeatures.split('&'))
            return True
        return False
        

    @pyknow.Rule(pyknow.Fact(action='consultationsFeature'),
            pyknow.OR(*Features.getNotFishFeatures()),
            salience=40)
    def askFeature(self, **kwargs):
        if self.declareNewFeatures():
            return

        oldFeatures = fishGlobals.request.POST.get('oldFeatures', '')
        idunnoFeatures = fishGlobals.request.POST.get('idunnoFeatures', '')
        ignoreFeatures = fishGlobals.request.POST.get('ignoreFeatures', '')

        featuresList = []
        if ignoreFeatures:
            ignoreFeatures = list(int(x) for x in ignoreFeatures.split('&'))
        else:
            ignoreFeatures = []
        if idunnoFeatures:
            idunnoFeatures = list(int(x) for x in idunnoFeatures.split('&'))
        else:
            idunnoFeatures = []

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

        print('featuresList:', featuresList)
        featuresList = featuresList[0:5]
        print('featuresList:', featuresList)
        newIdunnoFeatures = ''
        newIgnoreFeatures = ''
        for feature in featuresList:
            if newIdunnoFeatures == '':
                newIdunnoFeatures = '{}'.format(feature.id)
            else:
                newIdunnoFeatures += '&{}'.format(feature.id)
            if newIgnoreFeatures == '':
                newIgnoreFeatures = '{}'.format(feature.id)
            else:
                newIgnoreFeatures += '&{}'.format(feature.id)

        if featuresList:
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
