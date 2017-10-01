from django.db import models
from django.shortcuts import render
from django.template import Context, RequestContext
from main.djangoModels.fish import fish


import pyknow

class Fish(pyknow.Fact):
    pass
    # self.fishData = fish.Fish.objects.all()

class FishDetachment(pyknow.Fact):
    # TODO: get facts from DB
    pass
class FishKind(pyknow.Fact):
    # TODO: get facts from DB
    pass
class FishFeature(pyknow.Fact):
    # TODO: get facts from DB
    pass

class FishEngine(pyknow.KnowledgeEngine):
    def setRequest(self, request):
        self.request = request

    @pyknow.DefFacts()
    def _initial_action(self):
        yield pyknow.Fact(action="fishing")

    # @pyknow.DefFacts()
    # def default_data(self):
    #     yield FishDetachment(detachment='carp')
    #     yield FishFeature(feature='lips with 4 mustaches')

    # @pyknow.Rule(pyknow.Fact(action='fishing'),
    #         pyknow.NOT(FishDetachment(detachment="detachment" << pyknow.W())))
    # def ask_detachment(self):
    #     self.declare(FishDetachment(detachment='carp'))

    # @pyknow.Rule(pyknow.Fact(action='fishing'),
    #         pyknow.NOT(FishFeature(feature="feature" << pyknow.W())))
    # def ask_feature(self):
    #     self.declare(FishFeature(feature='lips with 4 mustaches'))

    @pyknow.Rule(pyknow.Fact(action='fishing'),
            Fish(detachment='carp'),
            Fish(feature='lips with 4 mustaches'))
    def carp(self, **kwargs):
        self.getGraph()
        self.response = render(self.request, 'labs/fish.html', {
            'fishName': 'carp',
            'facts': self.facts,
        })


    def getGraph(self, path="../full_static/graph/fish.gv", view=False):
        graph = self.matcher.show_network()
        graph.format = 'svg'
        graph.render(path, view=False)

