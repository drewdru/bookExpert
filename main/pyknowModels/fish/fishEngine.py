from django.db import models
from django.shortcuts import render
from django.template import Context
from django.http.request import HttpRequest
from main.djangoModels.fish import fishFeature, fishKind
from .facts.features import Features
from .facts.kinds import Kinds

import pyknow
import random

MODULE_REQUEST = HttpRequest()
FISH_FEATURES = fishFeature.FishFeature.objects.all()
FISH_KIND = fishKind.FishKind.objects.all()

class FishEngine(pyknow.KnowledgeEngine):
    @pyknow.DefFacts()
    def _initial_action(self):
        # yield pyknow.Fact(action='answerKind')
        yield pyknow.Fact(action='consultationsFeature')
        yield pyknow.Fact(action='fishing')

    def changePostParametrs(self):
        mutable = MODULE_REQUEST.POST._mutable
        MODULE_REQUEST.POST._mutable = True
        MODULE_REQUEST.POST['oldFeatures'] = self.oldFeatures
        MODULE_REQUEST.POST['ignoreFeatures'] = self.ignoreFeatures
        try:            
            MODULE_REQUEST.POST.pop('feature')
        except KeyError:
            pass
        MODULE_REQUEST.POST._mutable = mutable

    # # TODO: CHECK pyknow.NOT to pyknow.NOT(pyknow.EXIST)
    @pyknow.Rule(pyknow.Fact(action='fishing'),
            *Features.getNotFishFeatures(FISH_FEATURES), 
            salience=1)
    def askFeature(self):
        self.newFeature = MODULE_REQUEST.POST.get('feature', '')
        self.oldFeatures = MODULE_REQUEST.POST.get('oldFeatures', '')
        self.ignoreFeatures = MODULE_REQUEST.POST.get('ignoreFeatures', '')
        print('newFeature:', self.newFeature)
        if self.newFeature != '':
            print('oldFeatures:', self.oldFeatures)
            if self.oldFeatures == '':
                self.oldFeatures = self.newFeature
            else:
                self.oldFeatures += '&{}'.format(self.newFeature)
            print('oldFeatures:', self.oldFeatures)
            for feature in self.oldFeatures.split('&'):
                print('feature:', feature)
                self.declare(Features(feature=feature))
            self.changePostParametrs()
            return
        featuresList = []
        for fact in Features.getFishFeatures(FISH_FEATURES):
            if fact['feature'] not in self.oldFeatures.split('&') and\
                    fact['feature'] not in self.ignoreFeatures.split('&'):
                featuresList.append(fact)                
        # featuresList = featuresList[0:5]
        featuresToIgnore = ''
        for feature in featuresList:
            featuresToIgnore += '&{}'.format(feature['feature'])
        print('FEATURE!')
        self.response = render(MODULE_REQUEST, 'labs/askFeature.html', {
            'question': 'Does the fish has one of the next features?',
            'features': featuresList,
            'featuresToIgnore': featuresToIgnore,
            'answer_id': 'feature',
            'url': '/bookExpert/fish', 
        })

    @pyknow.Rule(pyknow.Fact(action='fishing'),
        pyknow.OR(*Kinds.getFishKinds(FISH_KIND)), 
        salience=10)
    def carp(self, **kwargs):
        self.getGraph()
        print('CARP!')
        self.response = render(MODULE_REQUEST, 'labs/fish.html', {
            'fishName': 'carp',
            'facts': self.facts,
        })

    def getGraph(self, path="../full_static/graph/fish.gv", view=False):
        graph = self.matcher.show_network()
        graph.format = 'svg'
        graph.render(path, view=False)

