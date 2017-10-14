
from django.shortcuts import render
from main.djangoModels.fish.fishFeature import FishFeature
from main.pyknowModels.fish.features import Features
from main.pyknowEngines.fish.baseEngine import BaseEngine
from main.pyknowEngines.fish import fishGlobals
# from main.pyknowEngines.fish.fishGlobals import FishGlobals

import pyknow

# REQUEST = HttpRequest()

class FeaturesEngine(BaseEngine):
    # @classmethod
    # def initRequest(cls, request):
    #     global REQUEST
    #     REQUEST = request

    def declareFeatures(self, features):
        for feature in features:
            self.declare(Features(feature=feature))

    @pyknow.Rule(pyknow.Fact(action='consultationsFeature'),
            pyknow.OR(*Features.getNotFishFeatures()),
            salience=40)
    def askFeature(self, **kwargs):
        newFeature = fishGlobals.request.POST.get('feature', '')
        oldFeatures = fishGlobals.request.POST.get('oldFeatures', '')

        idunnoFeatures = fishGlobals.request.POST.get('idunnoFeatures', '')
        newIdunnoList = fishGlobals.request.POST.get('newIdunnoList', '')
        
        ignoreFeatures = fishGlobals.request.POST.get('ignoreFeatures', '')
        newIgnoreList = fishGlobals.request.POST.get('newIgnoreList', '')

        if newFeature != '':
            if oldFeatures == '' and '_submit' in fishGlobals.request.POST:
                oldFeatures = newFeature
            elif '_submit' in fishGlobals.request.POST:
                oldFeatures += '&{}'.format(newFeature)
            if idunnoFeatures == '' and '_idunno' in fishGlobals.request.POST:
                    idunnoFeatures = newIdunnoList
            elif '_idunno' in fishGlobals.request.POST:
                idunnoFeatures += '&{}'.format(newIdunnoList)
            if ignoreFeatures == '' and '_no' in fishGlobals.request.POST:
                    ignoreFeatures = newIgnoreList
            elif '_no' in fishGlobals.request.POST:
                ignoreFeatures += '&{}'.format(newIgnoreList)                
            self.changePostParametrs(fishGlobals.request, {
                    'oldFeatures': oldFeatures,
                    'idunnoFeatures': idunnoFeatures,
                    'ignoreFeatures': ignoreFeatures
                }, ['feature'])
            if oldFeatures != '':
                self.declareFeatures(oldFeatures.split('&'))
            return

        featuresList = []
        if ignoreFeatures:
            ignoreFeatures = list(int(x) for x in ignoreFeatures.split('&'))
        else:
            ignoreFeatures = []

        print('ignoreFeatures', ignoreFeatures)
        for feature in FishFeature.objects.all().exclude(id__in=ignoreFeatures):
            if str(feature.id) not in oldFeatures.split('&') and\
                    str(feature.id) not in idunnoFeatures.split('&'):
                featuresList.append(feature)

        if not featuresList:
            for feature in FishFeature.objects.all().exclude(
                    id__in=ignoreFeatures):
                if str(feature.id) not in oldFeatures.split('&'):
                    featuresList.append(feature)            
            self.changePostParametrs(fishGlobals.request, {
                'idunnoFeatures': '',
                'newIdunnoList': '',
            }, [])

        featuresList = featuresList[0:5]

        newIdunnoList = ''
        newIgnoreList = ''
        for feature in featuresList:
            if newIdunnoList == '':
                newIdunnoList = '{}'.format(feature.id)
            else:
                newIdunnoList += '&{}'.format(feature.id)
            if newIgnoreList == '':
                newIgnoreList = '{}'.format(feature.id)
            else:
                newIgnoreList += '&{}'.format(feature.id)
        print('newIdunnoList', newIdunnoList)

        self.response = render(fishGlobals.request, 'labs/askFeature.html', {
            'question': 'Does the fish has one of the next features?',
            'features': featuresList,
            'newIdunnoList': newIdunnoList,
            'newIgnoreList': newIgnoreList,
            'answer_id': 'feature',
            'facts': self.facts,
            'url': '/bookExpert/fish', 
        })
