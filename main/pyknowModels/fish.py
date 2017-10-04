from django.db import models
from django.shortcuts import render
from django.template import Context, RequestContext
from django.http.request import HttpRequest
from main.djangoModels.fish import fish
from main.djangoModels.fish import fishDetachment
from main.djangoModels.fish import fishKind
from main.djangoModels.fish import fishFeature


import pyknow
import random

# def objGeneratorGenerator(objList):
#     for data in objList:
#         yield data
MODULE_REQUEST = HttpRequest()

def listToStr(fieldList):
    fields = []
    for field in fieldList:
        fields.append(str(field))
    return '&'.join(fields)


class FishFact(pyknow.Fact):
    @classmethod
    def from_django_model(cls, obj):
        detachments = listToStr(obj.detachments.all())
        features = listToStr(obj.features.all())
        kinds = listToStr(obj.kinds.all())
        return cls(fishName=obj.fishName,
                   detachments=detachments,
                   features=features,
                   kinds=kinds)

    @classmethod
    def getFishFacts(cls):
        factList = []
        for fishObject in fish.Fish.objects.all():
            factList.append(FishFact.from_django_model(fishObject))
        return factList

    def save_to_db(self):
        return fish.Fish.objects.create(**self)


class Detachments(pyknow.Fact):
    @classmethod
    def from_django_model(cls, obj):
        features = listToStr(obj.features.all())
        kinds = listToStr(obj.kinds.all())
        return cls(detachment=obj.detachment,
                   features=features,
                   kinds=kinds)

    @classmethod
    def getNotFishDetachments(cls):
        detachmentList = []
        for detachment in fishDetachment.FishDetachment.objects.all():
            detachmentList.append(pyknow.NOT(
                Detachments.from_django_model(detachment)))
        return detachmentList

    def save_to_db(self):
        return fishDetachment.FishDetachment.objects.create(**self)


class Kinds(pyknow.Fact):
    @classmethod
    def from_django_model(cls, obj):
        facts = []
        for feature in obj.features.all():
            facts.append(Features(feature=feature))
        facts.append(cls(kind=obj.kind))
        return facts

    @classmethod
    def getIgnoreKinds(cls):
        ignoreKinds = MODULE_REQUEST.POST.get('ignoreKinds', '')
        kindsList = []
        for kind in ignoreKinds.split('&'):
            for kinds in fishKind.FishKind.objects.all().filter(kind=kind):
                kindsList.append(pyknow.AND(*Kinds.from_django_model(kinds)))
        return kindsList if len(kindsList) > 0 else [pyknow.Fact()]

    @classmethod
    def getFishKinds(cls):
        kindsList = []
        for kinds in fishKind.FishKind.objects.all():
            kindsList.append(pyknow.AND(*Kinds.from_django_model(kinds)))
        return kindsList

    @classmethod
    def getNotFishKinds(cls):
        kindsList = []
        for kinds in fishKind.FishKind.objects.all():
            kindsList.append(pyknow.NOT(pyknow.AND(
                *Kinds.from_django_model(kinds))))
        return kindsList

    def save_to_db(self):
        return fishKind.FishKind.objects.create(**self)


class Features(pyknow.Fact):
    @classmethod
    def from_django_model(cls, obj):
        return cls(feature=obj.feature)

    @classmethod
    def getIgnoreFeatures(cls):
        ignoreFeatures = MODULE_REQUEST.POST.get('ignoreFeatures', '')
        featuresList = []
        for feature in ignoreFeatures.split('&'):
            featuresList.append(cls(feature=feature))
        return featuresList

    @classmethod
    def getFishFeatures(cls):
        featuresList = []
        for feature in fishFeature.FishFeature.objects.all():
            featuresList.append(Features.from_django_model(feature))
        return featuresList

    @classmethod
    def getNotFishFeatures(cls):
        featuresList = []
        for feature in fishFeature.FishFeature.objects.all():
            featuresList.append(pyknow.NOT(
                Features.from_django_model(feature)))
        return featuresList

class FishEngine(pyknow.KnowledgeEngine):
    def declareFeatures(self, features):
        for feature in features:
            self.declare(Features(feature=feature))

    def declareKinds(self, kinds):
        for kind in kinds:
            self.declare(Kinds(kind=kind))

    @pyknow.DefFacts()
    def _initial_action(self):
        yield pyknow.Fact(action="fishing")
        yield pyknow.Fact(action="consultationsFeature")
        yield pyknow.Fact(action="consultationsKind")
        
    
    def changeKindsPostParametrs(self, oldKinds, ignoreKinds):
        mutable = MODULE_REQUEST.POST._mutable
        MODULE_REQUEST.POST._mutable = True
        MODULE_REQUEST.POST['oldKinds'] = oldKinds
        MODULE_REQUEST.POST['ignoreKinds'] = ignoreKinds
        MODULE_REQUEST.POST.pop('kind')
        MODULE_REQUEST.POST._mutable = mutable

    # TODO: don't go into if kindsList is clear
    @pyknow.Rule(pyknow.Fact(action='consultationsKind'),
            pyknow.AND(pyknow.NOT(*Kinds.getIgnoreKinds()),
            pyknow.OR(*Kinds.getNotFishKinds())))
    def askKind(self):
        newKind = MODULE_REQUEST.POST.get('kind', '')
        oldKinds = MODULE_REQUEST.POST.get('oldKinds', '')
        ignoreKinds = MODULE_REQUEST.POST.get('ignoreKinds', '')
        if newKind != '':
            if oldKinds == '':
                oldKinds = newKind
            else:
                oldKinds += '&{}'.format(newKind)
            self.changeKindsPostParametrs(oldKinds, ignoreKinds)
            self.declareKinds(oldKinds.split('&'))
            return

        kindsList = []
        for facts in Kinds.getFishKinds():
            for fact in facts:
                if 'kind' in fact and  fact['kind'] not in oldKinds.split('&') and\
                        fact['kind'] not in ignoreKinds.split('&'):
                    kindsList.append(fact)                
        kindsList = kindsList[0:5]
        kindsStr = ''
        for kind in kindsList:
            kindsStr += '&{}'.format(kind['kind'])

        self.response = render(MODULE_REQUEST, 'labs/askKind.html', {
            'question': 'Does the fish has one of the next kinds?',
            'kinds': kindsList,
            'kindsStr': kindsStr,
            'answer_id': 'kind',
            'url': '/bookExpert/fish', 
        })

    @pyknow.Rule(pyknow.Fact(action='fishing'),
            pyknow.OR(*Kinds.getFishKinds()))
    def answerKind(self, **kwargs):
        self.getGraph()
        try:
            fishName = self.facts.get(self.facts.last_index-1)['fishName']
        except Exception as error:
            print(error)
            fishName = False
        self.response = render(MODULE_REQUEST, 'labs/fish.html', {
            'fishName': fishName,
            'facts': self.facts,
        })


    def changeFeaturePostParametrs(self, oldFeatures, ignoreFeatures):
        mutable = MODULE_REQUEST.POST._mutable
        MODULE_REQUEST.POST._mutable = True
        MODULE_REQUEST.POST['oldFeatures'] = oldFeatures
        MODULE_REQUEST.POST['ignoreFeatures'] = ignoreFeatures
        MODULE_REQUEST.POST.pop('feature')
        MODULE_REQUEST.POST._mutable = mutable

    @pyknow.Rule(pyknow.Fact(action='consultationsFeature'),
            pyknow.AND(pyknow.NOT(*Features.getIgnoreFeatures()),
            pyknow.OR(*Features.getNotFishFeatures())))
    def askFeature(self):
        newFeature = MODULE_REQUEST.POST.get('feature', '')
        oldFeatures = MODULE_REQUEST.POST.get('oldFeatures', '')
        ignoreFeatures = MODULE_REQUEST.POST.get('ignoreFeatures', '')
        if newFeature != '':
            if oldFeatures == '':
                oldFeatures = newFeature
            else:
                oldFeatures += '&{}'.format(newFeature)
            self.changeFeaturePostParametrs(oldFeatures, ignoreFeatures)
            self.declareFeatures(oldFeatures.split('&'))
            return

        featuresList = []
        for fact in Features.getFishFeatures():
            if fact['feature'] not in oldFeatures.split('&') and\
                    fact['feature'] not in ignoreFeatures.split('&'):
                featuresList.append(fact)                
        featuresList = featuresList[0:5]
        featuresToIgnore = ''
        for feature in featuresList:
            featuresToIgnore += '&{}'.format(feature['feature'])

        self.response = render(MODULE_REQUEST, 'labs/askFeature.html', {
            'question': 'Does the fish has one of the next features?',
            'features': featuresList,
            'featuresToIgnore': featuresToIgnore,
            'answer_id': 'feature',
            'url': '/bookExpert/fish', 
        })

    @pyknow.Rule(pyknow.Fact(action='fishing'),
            pyknow.OR(*Features.getFishFeatures()))
    def answerFeature(self, **kwargs):
        self.getGraph()
        try:
            fishName = self.facts.get(self.facts.last_index-1)['fishName']
        except Exception as error:
            print(error)
            fishName = False
        self.response = render(MODULE_REQUEST, 'labs/fish.html', {
            'fishName': fishName,
            'facts': self.facts,
            'url': '/bookExpert/fish', 
        })

    @pyknow.Rule(pyknow.Fact(action='fishing'),
            pyknow.OR(*FishFact.getFishFacts()))
    def answerFish(self, **kwargs):
        self.getGraph()
        try:
            fishName = self.facts.get(self.facts.last_index-1)['fishName']
        except Exception as error:
            print(error)
            fishName = False
        self.response = render(MODULE_REQUEST, 'labs/fish.html', {
            'fishName': fishName,
            'facts': self.facts,
        })

    def getGraph(self, path="../full_static/graph/fish.gv", view=False):
        graph = self.matcher.show_network()
        graph.format = 'svg'
        graph.render(path, view=False)

