# https://github.com/vulogov/clips6/
# http://pyclips.sourceforge.net/web/?q=node/25 
from django.db import models
from django.shortcuts import render
from django.template import Context
from django.http.request import HttpRequest

from main.djangoModels.fish import fishFeature
from main.djangoModels.fish import fishKind


from .facts.features import Features
from .facts.kinds import Kinds

import pyknow
import random

MODULE_REQUEST = HttpRequest()
FISH_FEATURES = fishFeature.FishFeature.objects.all()
FISH_KIND = fishKind.FishKind.objects.all()

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
        # for fact in Features.getFishFeatures(FISH_FEATURES):
        #     if fact['feature'] not in oldFeatures.split('&') and\
        #             fact['feature'] not in ignoreFeatures.split('&'):
        #         featuresList.append(fact)
        for feature in FISH_FEATURES:
            if str(feature.id) not in oldFeatures.split('&') and\
                    str(feature.id) not in ignoreFeatures.split('&'):
                featuresList.append(feature.id)
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

    @pyknow.Rule(pyknow.Fact(action='fishing'),
            pyknow.OR(*Kinds.getFishKinds(FISH_KIND)),
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

    def getGraph(self, path="../full_static/graph/fish.gv", view=False):
        graph = self.matcher.show_network()
        graph.format = 'svg'
        graph.render(path, view=False)

    # @pyknow.Rule(pyknow.Fact(action='fishing'),
    #         pyknow.OR(pyknow.AND(Features(feature='lips with 4 mustaches'),
    #                 Features(feature='fish swim in rivers or lakes')),
    #             pyknow.AND(Features(feature='lips with 4 mustaches'),
    #                 Features(feature='fish swim in rivers or lakes')),
    #         ),
    #         salience=2)
    # def answerTest(self, **kwargs):
    #     self.getGraph()
    #     try:
    #         fishName = self.facts.get(self.facts.last_index-1)['fishName']
    #     except Exception as error:
    #         print(error)
    #         fishName = False
    #     self.response = render(MODULE_REQUEST, 'labs/fish.html', {
    #         'fishName': '''fish with lips with 4 mustaches AND fish swim in \
    #                         rivers or lake OR lips with 4 mustaches AND \
    #                         fish swim in rivers or lakes''',
    #         'facts': self.facts,
    #         'url': '/bookExpert/fish', 
    #     })

# from django.db import models
# from django.shortcuts import render
# from django.template import Context
# from django.http.request import HttpRequest

# from main.djangoModels.fish import fishFeature
# from main.djangoModels.fish import fishKind


# from .facts.features import Features
# from .facts.kinds import Kinds

# import pyknow
# import random

# MODULE_REQUEST = HttpRequest()
# FISH_FEATURES = fishFeature.FishFeature.objects.all()
# FISH_KIND = fishKind.FishKind.objects.all()

# class FishEngine(pyknow.KnowledgeEngine):
#     def declareFeatures(self, features):
#         for feature in features:
#             self.declare(Features(feature=feature))

#     def declareKinds(self, kinds):
#         for kind in kinds:
#             self.declare(Kinds(kind=kind))

#     @pyknow.DefFacts()
#     def _initial_action(self):
#         yield pyknow.Fact(action="fishing")
#         yield pyknow.Fact(action="consultationsFeature")
#         yield pyknow.Fact(action="consultationsKind")
        
    
#     def changeKindsPostParametrs(self, oldKinds, ignoreKinds):
#         mutable = MODULE_REQUEST.POST._mutable
#         MODULE_REQUEST.POST._mutable = True
#         MODULE_REQUEST.POST['oldKinds'] = oldKinds
#         MODULE_REQUEST.POST['ignoreKinds'] = ignoreKinds
#         MODULE_REQUEST.POST.pop('kind')
#         MODULE_REQUEST.POST._mutable = mutable

#     # TODO: don't go into if kindsList is clear
#     @pyknow.Rule(pyknow.Fact(action='consultationsKind'),
#             pyknow.NOT(*Kinds.getIgnoreKinds(MODULE_REQUEST, FISH_KIND)),
#             *Kinds.getNotFishKinds(FISH_KIND))
#     def askKind(self):
#         newKind = MODULE_REQUEST.POST.get('kind', '')
#         oldKinds = MODULE_REQUEST.POST.get('oldKinds', '')
#         ignoreKinds = MODULE_REQUEST.POST.get('ignoreKinds', '')
#         if newKind != '':
#             if oldKinds == '':
#                 oldKinds = newKind
#             else:
#                 oldKinds += '&{}'.format(newKind)
#             self.changeKindsPostParametrs(oldKinds, ignoreKinds)
#             self.declareKinds(oldKinds.split('&'))
#             return

#         kindsList = []
#         for facts in Kinds.getFishKinds(FISH_KIND):
#             for fact in facts:
#                 if 'kind' in fact and  fact['kind'] not in oldKinds.split('&') and\
#                         fact['kind'] not in ignoreKinds.split('&'):
#                     kindsList.append(fact)                
#         kindsList = kindsList[0:5]
#         kindsStr = ''
#         for kind in kindsList:
#             kindsStr += '&{}'.format(kind['kind'])

#         self.response = render(MODULE_REQUEST, 'labs/askKind.html', {
#             'question': 'Does the fish has one of the next kinds?',
#             'kinds': kindsList,
#             'kindsStr': kindsStr,
#             'answer_id': 'kind',
#             'url': '/bookExpert/fish', 
#         })

#     @pyknow.Rule(pyknow.Fact(action='fishing'),
#             pyknow.OR(*Kinds.getFishKinds(FISH_KIND)))
#     def answerKind(self, **kwargs):
#         self.getGraph()
#         try:
#             fishName = self.facts.get(self.facts.last_index-1)['fishName']
#         except Exception as error:
#             print(error)
#             fishName = False
#         self.response = render(MODULE_REQUEST, 'labs/fish.html', {
#             'fishName': fishName,
#             'facts': self.facts,
#         })


#     def changeFeaturePostParametrs(self, oldFeatures, ignoreFeatures):
#         mutable = MODULE_REQUEST.POST._mutable
#         MODULE_REQUEST.POST._mutable = True
#         MODULE_REQUEST.POST['oldFeatures'] = oldFeatures
#         MODULE_REQUEST.POST['ignoreFeatures'] = ignoreFeatures
#         MODULE_REQUEST.POST.pop('feature')
#         MODULE_REQUEST.POST._mutable = mutable

#     @pyknow.Rule(pyknow.Fact(action='consultationsFeature'),
#             pyknow.NOT(*Features.getIgnoreFeatures(MODULE_REQUEST),
#             *Features.getNotFishFeatures(FISH_FEATURES)))
#     def askFeature(self):
#         newFeature = MODULE_REQUEST.POST.get('feature', '')
#         oldFeatures = MODULE_REQUEST.POST.get('oldFeatures', '')
#         ignoreFeatures = MODULE_REQUEST.POST.get('ignoreFeatures', '')
#         if newFeature != '':
#             if oldFeatures == '':
#                 oldFeatures = newFeature
#             else:
#                 oldFeatures += '&{}'.format(newFeature)
#             self.changeFeaturePostParametrs(oldFeatures, ignoreFeatures)
#             self.declareFeatures(oldFeatures.split('&'))
#             return

#         featuresList = []
#         for fact in Features.getFishFeatures(FISH_FEATURES):
#             if fact['feature'] not in oldFeatures.split('&') and\
#                     fact['feature'] not in ignoreFeatures.split('&'):
#                 featuresList.append(fact)                
#         featuresList = featuresList[0:5]
#         featuresToIgnore = ''
#         for feature in featuresList:
#             featuresToIgnore += '&{}'.format(feature['feature'])

#         self.response = render(MODULE_REQUEST, 'labs/askFeature.html', {
#             'question': 'Does the fish has one of the next features?',
#             'features': featuresList,
#             'featuresToIgnore': featuresToIgnore,
#             'answer_id': 'feature',
#             'url': '/bookExpert/fish', 
#         })

#     @pyknow.Rule(pyknow.Fact(action='fishing'),
#             pyknow.OR(*Features.getFishFeatures(FISH_FEATURES)))
#     def answerFeature(self, **kwargs):
#         self.getGraph()
#         try:
#             fishName = self.facts.get(self.facts.last_index-1)['fishName']
#         except Exception as error:
#             print(error)
#             fishName = False
#         self.response = render(MODULE_REQUEST, 'labs/fish.html', {
#             'fishName': fishName,
#             'facts': self.facts,
#             'url': '/bookExpert/fish', 
#         })

#     # @pyknow.Rule(pyknow.Fact(action='fishing'),
#     #         pyknow.OR(*FishFact.getFishFacts()))
#     # def answerFish(self, **kwargs):
#     #     self.getGraph()
#     #     try:
#     #         fishName = self.facts.get(self.facts.last_index-1)['fishName']
#     #     except Exception as error:
#     #         print(error)
#     #         fishName = False
#     #     self.response = render(MODULE_REQUEST, 'labs/fish.html', {
#     #         'fishName': fishName,
#     #         'facts': self.facts,
#     #     })

#     def getGraph(self, path="../full_static/graph/fish.gv", view=False):
#         graph = self.matcher.show_network()
#         graph.format = 'svg'
#         graph.render(path, view=False)

