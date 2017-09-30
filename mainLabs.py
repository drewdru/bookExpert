import sys

import pyknow

class Greetings(pyknow.KnowledgeEngine):
    @pyknow.DefFacts()
    def _initial_action(self):
        yield pyknow.Fact(action="greet")

    @pyknow.Rule(pyknow.Fact(action='greet'),
          pyknow.NOT(pyknow.Fact(name=pyknow.W())))
    def ask_name(self):
        self.declare(pyknow.Fact(name=input("What's your name? ")))

    @pyknow.Rule(pyknow.Fact(action='greet'),
          pyknow.NOT(pyknow.Fact(location=pyknow.W())))
    def ask_location(self):
        self.declare(pyknow.Fact(location=input("Where are you? ")))

    @pyknow.Rule(pyknow.Fact(action='greet'),
          pyknow.Fact(name="name" << pyknow.W()),
          pyknow.Fact(location="location" << pyknow.W()))
    def greet(self, name, location):
        print("Hi %s! How is the weather in %s?" % (name, location))


class Factorial(pyknow.Fact):
    pass
def isint(x):
    return isinstance(x, int)    
class ComputeFactorial(pyknow.KnowledgeEngine):    
    @pyknow.Rule(Factorial('x' << pyknow.P(isint),
                    'y' << pyknow.P(isint)))
    def factorial(self, x, y):
        self.declare(Factorial(x + 1, (x + 1) * y))

def main():
    greetingsEngine = Greetings()
    greetingsEngine.reset()  # Prepare the engine for the execution.
    greetingsEngine.run()  # Run it!

    factorialEngine = ComputeFactorial()
    factorialEngine.reset()
    factorialEngine.declare(Factorial(1, 1))
    factorialEngine.run(10)
    print(factorialEngine.facts)
    graph = factorialEngine.matcher.show_network()
    print(graph.source)
    # graph.render('./Temp/round-table.gv', view=True) # sudo apt-get install graphviz




if __name__ == '__main__':
    sys.exit(main())
