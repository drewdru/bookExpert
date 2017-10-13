# https://github.com/vulogov/clips6/
# http://pyclips.sourceforge.net/web/?q=node/25 
from django.db import models
from django.shortcuts import render
from django.template import Context
from django.http.request import HttpRequest

from main.djangoModels.fish import fishFeature
from main.djangoModels.fish import fishKind

from main.pyknowEngines.fish.featuresEngine import FeaturesEngine
from main.pyknowEngines.fish.kindsEngine import KindsEngine

import pyknow

class FishEngine(FeaturesEngine, KindsEngine):
    def initRequest(self, request):
        FeaturesEngine.initRequest(request)
        KindsEngine.initRequest(request)

    @pyknow.DefFacts()
    def _initial_action(self):
        yield pyknow.Fact(action="answerKind")
        yield pyknow.Fact(action="consultationsFeature")
