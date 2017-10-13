
from django.shortcuts import render
from main.djangoModels.fish.fishKind import FishKind
from main.pyknowModels.fish.kinds import Kinds
from main.pyknowEngines.fish.baseEngine import BaseEngine

import pyknow
import random

class KindsEngine(BaseEngine):
    def declareKinds(self, kinds):
        for kind in kinds:
            self.declare(Kinds(kind=kind))

    @pyknow.Rule(pyknow.Fact(action='answerKind'),
            pyknow.OR(*Kinds.getKindsFeatures()),
            salience=30)
    def answerKind(self, **kwargs):
        featureList = []
        for key, value in kwargs.items():
            if key.startswith('feature_'):
                featureList.append(int(value['feature']))
        kinds = FishKind.objects.all().filter(features__in=featureList)
        kind= random.choice(kinds)
        self.getGraph()
        self.response = render(KindsEngine.request, 'labs/fish.html', {
            'amswer': kind.kind,
            'facts': self.facts,
            'url': '/bookExpert/fish', 
        })
