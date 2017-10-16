# https://github.com/vulogov/clips6/
# http://pyclips.sourceforge.net/web/?q=node/25
from main.pyknowEngines.fish.featuresEngine import FeaturesEngine
from main.pyknowEngines.fish.kindsEngine import KindsEngine
from main.pyknowEngines.fish import fishGlobals

import pyknow

class FishEngine(FeaturesEngine, KindsEngine):
    @pyknow.DefFacts()
    def _initial_action(self):
        # yield pyknow.Fact(action='answerDetachment')
        yield pyknow.Fact(action='answerKind')
        yield pyknow.Fact(action='consultationsKind')
        yield pyknow.Fact(action='consultationsFeature')
