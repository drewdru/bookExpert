from django.db import models
# Create your models here.
import pyknow

def isint(x):
    return isinstance(x, int)

class Factorial(pyknow.Fact):
    pass

class ComputeFactorial(pyknow.KnowledgeEngine):
    @pyknow.Rule(Factorial('x' << pyknow.P(isint),
                    'y' << pyknow.P(isint)))
    def factorial(self, x, y):
        self.declare(Factorial(x + 1, (x + 1) * y))

    def getGraph(self, path="../full_static/graph/factorial.gv", view=False):
        graph = self.matcher.show_network()
        graph.format = 'svg'
        graph.render(path, view=False)
