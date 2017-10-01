from django.db import models
from django.shortcuts import render
from django.template import Context, RequestContext
import pyknow

class Greetings(pyknow.KnowledgeEngine):
    def setRequest(self, request):
        self.request = request
        self.response = render(self.request, 'labs/greetings.html', {})

    @pyknow.DefFacts()
    def _initial_action(self):
        yield pyknow.Fact(action="greet")

    @pyknow.Rule(pyknow.Fact(action='greet'),
          pyknow.NOT(pyknow.Fact(name=pyknow.W())))
    def ask_name(self):
        name = self.request.POST.get("name", None)
        if name is None:
            self.response = render(self.request, 'ask.html', {
                'question': "What's your name?",
                'answer_id': 'name',
                'url': '/bookExpert/greetings',
            })
        else:
            self.declare(pyknow.Fact(name=name))

    @pyknow.Rule(pyknow.Fact(action='greet'),
          pyknow.NOT(pyknow.Fact(location=pyknow.W())))
    def ask_location(self):
        # location = self.request.GET.get("location", "Russia")
        location = self.request.POST.get("location", None)
        if location is None:
            self.response = render(self.request, 'ask.html', {
                'question': "Where are you?",
                'answer_id': 'location',
                'url': '/bookExpert/greetings',
            })
        else:
            self.declare(pyknow.Fact(location=location))

    @pyknow.Rule(pyknow.Fact(action='greet'),
          pyknow.Fact(name="name" << pyknow.W()),
          pyknow.Fact(location="location" << pyknow.W()))
    def greet(self, name, location):
        self.getGraph()
        self.response = render(self.request, 'labs/greetings.html', {
            'name': name,
            'location': location,
            'facts': self.facts,
        })

    def getGraph(self, path="../full_static/graph/greetings.gv", view=False):
        graph = self.matcher.show_network()
        graph.format = 'svg'
        graph.render(path, view=False)
