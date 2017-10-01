import sys

import pyknow


    #     yield pyknow.Fact(action="fish")
    #     yield pyknow.Fact(action="otrajd")
    #     yield pyknow.Fact(action="vid")
    #     yield pyknow.Fact(action="priznak")

    # @pyknow.Rule(pyknow.Fact(action='fish'),
    #       pyknow.Fact(name="name" << "cазан"),
    #       pyknow.Fact(name="otrajd" << "карпообразные"),
    #       pyknow.Fact(name="priznak" << "губы с 4 усиками"),)

class Greetings(pyknow.KnowledgeEngine):
    @pyknow.DefFacts()
    def _initial_action(self):
        yield pyknow.Fact(action="greet")

    @pyknow.Rule(pyknow.Fact(action='greet'),
          pyknow.NOT(pyknow.Fact(name=pyknow.W())))
    def ask_name(self):
        # self.declare(pyknow.Fact(name=input("What's your name? ")))
        self.declare(pyknow.Fact(name="NAME"))

    @pyknow.Rule(pyknow.Fact(action='greet'),
          pyknow.NOT(pyknow.Fact(location=pyknow.W())))
    def ask_location(self):
        # self.declare(pyknow.Fact(location=input("Where are you? ")))
        self.declare(pyknow.Fact(location="RUSSIA"))

    @pyknow.Rule(pyknow.Fact(action='greet'),
          pyknow.Fact(name="name" << pyknow.W()),
          pyknow.Fact(location="location" << pyknow.W()))
    def greet(self, name, location):
        print("Hi %s! How is the weather in %s?" % (name, location))



class Fish(pyknow.Fact):
    pass
class Otrajd(pyknow.Fact):
    pass
class Priznak(pyknow.Fact):
    pass
class Vid(pyknow.Fact):
    pass


def main():
    greetingsEngine = Greetings()
    greetingsEngine.reset()  # Prepare the engine for the execution.
    greetingsEngine.run()  # Run it!
    # print(greetingsEngine.facts)
    # graph = greetingsEngine.matcher.show_network()
    # print(graph.source)

    # graph.render('./Temp/round-table.gv', view=True) # sudo apt-get install graphviz


if __name__ == '__main__':
    sys.exit(main())
