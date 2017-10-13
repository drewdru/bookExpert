from django.db import models
# Create your models here.
import pyknow

def isint(x):
    return isinstance(x, int)

class ComputeFactorial(pyknow.KnowledgeEngine):    
    @pyknow.DefFacts()
    def _initial_action(self):
        yield pyknow.Fact(1, 1)

    @pyknow.Rule(pyknow.Fact('x' << pyknow.P(isint),
                    'y' << pyknow.P(isint)))
    def factorial(self, x, y):
        self.declare(pyknow.Fact(x + 1, (x + 1) * y))

    def getGraph(self, path="../full_static/graph/factorial.gv", view=False):
        graph = self.matcher.show_network()
        graph.format = 'svg'
        graph.render(path, view=False)
