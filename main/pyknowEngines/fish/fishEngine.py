# https://github.com/vulogov/clips6/
# http://pyclips.sourceforge.net/web/?q=node/25 
from django.db import models
from django.shortcuts import render
from django.template import Context
from django.http.request import HttpRequest

from main.djangoModels.fish import fishFeature
from main.djangoModels.fish import fishKind

from main.pyknowModels.fish.features import Features
from main.pyknowModels.fish.kinds import Kinds

import pyknow
import random

MODULE_REQUEST = HttpRequest()
FISH_FEATURES = fishFeature.FishFeature.objects.all()
FISH_KIND = fishKind.FishKind.objects.all()

class FeaturesEngine(pyknow.KnowledgeEngine):
    def declareFeatures(self, features):
        for feature in features:
            self.declare(Features(feature=feature))

    def changeFeaturePostParametrs(self, oldFeatures, ignoreFeatures):
        mutable = MODULE_REQUEST.POST._mutable
        MODULE_REQUEST.POST._mutable = True
        MODULE_REQUEST.POST['oldFeatures'] = oldFeatures
        MODULE_REQUEST.POST['ignoreFeatures'] = ignoreFeatures
        MODULE_REQUEST.POST.pop('feature')
        MODULE_REQUEST.POST._mutable = mutable

    @pyknow.Rule(pyknow.Fact(action='consultationsFeature'),
            pyknow.OR(*Features.getNotFishFeatures(FISH_FEATURES)),
            salience=3)
            # pyknow.AND(*Features.getIgnoreFeatures(MODULE_REQUEST)),
            # pyknow.OR(*Features.getNotFishFeatures(FISH_FEATURES)))
    def askFeature(self, **kwargs):
        newFeature = MODULE_REQUEST.POST.get('feature', '')
        oldFeatures = MODULE_REQUEST.POST.get('oldFeatures', '')
        ignoreFeatures = MODULE_REQUEST.POST.get('ignoreFeatures', '')
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
            self.changeFeaturePostParametrs(oldFeatures, ignoreFeatures)
            self.declareFeatures(oldFeatures.split('&'))
            return

        featuresList = []
        for feature in FISH_FEATURES:
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

        self.response = render(MODULE_REQUEST, 'labs/askFeature.html', {
            'question': 'Does the fish has one of the next features?',
            'features': featuresList,
            'featuresToIgnore': featuresToIgnore,
            'answer_id': 'feature',
            'facts': self.facts,
            'url': '/bookExpert/fish', 
        })

class KindsEngine(pyknow.KnowledgeEngine):
    @pyknow.Rule(pyknow.Fact(action='answerKind'),
            pyknow.OR(*Kinds.getKindsFeatures(FISH_KIND)),
            salience=2)
    def answerKind(self, **kwargs):
        featureList = []
        for key, value in kwargs.items():
            if key.startswith('feature_'):
                featureList.append(int(value['feature']))
        kinds = FISH_KIND.filter(features__in=featureList)
        kind= random.choice(kinds)
        self.response = render(MODULE_REQUEST, 'labs/fish.html', {
            'fishName': kind.kind,
            'facts': self.facts,
            'url': '/bookExpert/fish', 
        })

class FishEngine(FeaturesEngine, KindsEngine):
    def declareKinds(self, kinds):
        for kind in kinds:
            self.declare(Kinds(kind=kind))

    @pyknow.DefFacts()
    def _initial_action(self):
        yield pyknow.Fact(action="answerKind")
        yield pyknow.Fact(action="consultationsFeature")

    def getGraph(self, path="../full_static/graph/fish.gv", view=False):
        graph = self.matcher.show_network()
        graph.format = 'svg'
        graph.render(path, view=False)
