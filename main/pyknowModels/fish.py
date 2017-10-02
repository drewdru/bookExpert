from django.db import models
from django.shortcuts import render
from django.template import Context, RequestContext
from main.djangoModels.fish import fish
from main.djangoModels.fish import fishDetachment
from main.djangoModels.fish import fishKind
from main.djangoModels.fish import fishFeature


import pyknow
import random

# def objGeneratorGenerator(objList):
#     for data in objList:
#         yield data

def listToStr(fieldList):
    fields = []
    for field in fieldList:
        fields.append(str(field))
    return '&'.join(fields)


class FishFact(pyknow.Fact):
    @classmethod
    def from_django_model(cls, obj):
        detachments = listToStr(obj.detachments.all())
        features = listToStr(obj.features.all())
        kinds = listToStr(obj.kinds.all())
        return cls(fishName=obj.fishName,
                   detachments=detachments,
                   features=features,
                   kinds=kinds)

    @classmethod
    def getFishFacts(cls):
        factList = []
        for fishObject in fish.Fish.objects.all():
            factList.append(FishFact.from_django_model(fishObject))
        return factList

    def save_to_db(self):
        return fish.Fish.objects.create(**self)


class Detachments(pyknow.Fact):
    @classmethod
    def from_django_model(cls, obj):
        features = listToStr(obj.features.all())
        kinds = listToStr(obj.kinds.all())
        return cls(detachment=obj.detachment,
                   features=features,
                   kinds=kinds)

    @classmethod
    def getNotFishDetachments(cls):
        detachmentList = []
        for detachment in fishDetachment.FishDetachment.objects.all():
            detachmentList.append(pyknow.NOT(
                Detachments.from_django_model(detachment)))
        return detachmentList

    def save_to_db(self):
        return fishDetachment.FishDetachment.objects.create(**self)


class Kinds(pyknow.Fact):
    @classmethod
    def from_django_model(cls, obj):
        features = listToStr(obj.features.all())
        return cls(kind=obj.kind,
                   features=features)

    @classmethod
    def getNotFishKinds(cls):
        kindsList = []
        for kinds in fishKind.FishKind.objects.all():
            kindsList.append(pyknow.NOT(
                Detachments.from_django_model(kinds)))
        return kindsList

    def save_to_db(self):
        return fishKind.FishKind.objects.create(**self)


class Features(pyknow.Fact):
    @classmethod
    def from_django_model(cls, obj):
        return cls(feature=obj.feature)


    @classmethod
    def getFishFeatures(cls):
        featuresList = []
        for feature in fishFeature.FishFeature.objects.all():
            featuresList.append(Features.from_django_model(feature))
        return featuresList

    @classmethod
    def getNotFishFeatures(cls):
        featuresList = []
        for feature in fishFeature.FishFeature.objects.all():
            featuresList.append(pyknow.NOT(
                Features.from_django_model(feature)))
        return featuresList

    def save_to_db(self):
        return fishFeature.FishFeature.objects.create(**self)

class FishEngine(pyknow.KnowledgeEngine):
    def setRequest(self, request):
        self.request = request

    # @classmethod
    # def declareCls(cls, obj):
    #     cls.declare(obj)
    def declareFeatures(self, features):
        for feature in features:
            # self.declare(pyknow.Fact(location=location))
            self.declare(Features(feature=feature))

    @pyknow.DefFacts()
    def _initial_action(self):
        yield pyknow.Fact(action="fishing")
        yield pyknow.Fact(action="consultations")

    # @pyknow.DefFacts()
    # def default_data(self):
    #     yield FishFact.from_django_model(fish.Fish.objects.all().first())

    # @pyknow.Rule(pyknow.Fact(action='consultations'),
    #     # pyknow.AND(
    #     #     pyknow.NOT(pyknow.Fact(location=pyknow.W()),
    #         # pyknow.NOT(pyknow.Fact(action=pyknow.W()))
    #         # pyknow.NOT(Fish.from_django_model(fish.Fish.objects.all().first()))
    #         # pyknow.NOT(pyknow.Fact(fishName=Fish.from_django_model(
    #         #     fish.Fish.objects.all().first())['fishName'])
    #         pyknow.NOT(pyknow.Fact(fishName=pyknow.W()))
    #     )
    @pyknow.Rule(pyknow.Fact(action='consultations'),
            pyknow.OR(*Features.getNotFishFeatures()))
    def askDetachment(self):
        # TODO: Declare NEW Detechments FACT and ask NEXT
        oldFeature = self.request.POST.get("features", None)
        if oldFeature is not None:
            print(oldFeature)
            self.declareFeatures(oldFeature.split('&'))
        # else:
        #     self.declareFeatures(['fins with pink feathers', 'test'])
        # # getNewFeauters

        # notAskedFeatures = ''
        # print(self.facts.items())
        # featuresList = []
        # for index, fact in enumerate(self.facts):
        #     temp = self.facts.get(index)
        #     if isinstance(temp, Features):
        #         featuresList.append(temp)
        # print(featuresList[0])
        # print(Features.getFishFeatures()[0])
        # print(featuresList[0] in Features.getFishFeatures()[0])
        # print('featuresList:', featuresList)
        # newFeatures = [x for x in Features.getFishFeatures() if x not in featuresList]
        # print('newFeatures:', newFeatures)
        featuresList = []
        for fact in Features.getFishFeatures():
            if fact.__factid__ is None:
                featuresList.append(fact)

        self.response = render(self.request, 'ask.html', {
            'question': "Does the fish has a feature: {}?".format(
                random.choice(featuresList)['feature']),
            'answer_id': 'feature',
            'url': '/bookExpert/fish',
        })


    @pyknow.Rule(pyknow.Fact(action='fishing'),
            pyknow.OR(*Features.getFishFeatures()))
    def answerFeature(self, **kwargs):
        self.getGraph()
        try:
            fishName = self.facts.get(self.facts.last_index-1)['fishName']
        except Exception as error:
            print(error)
            fishName = False
        self.response = render(self.request, 'labs/fish.html', {
            'fishName': fishName,
            'facts': self.facts,
        })


    @pyknow.Rule(pyknow.Fact(action='fishing'),
            pyknow.OR(*FishFact.getFishFacts()))
    def answerFish(self, **kwargs):
        self.getGraph()
        try:
            fishName = self.facts.get(self.facts.last_index-1)['fishName']
        except Exception as error:
            print(error)
            fishName = False
        self.response = render(self.request, 'labs/fish.html', {
            'fishName': fishName,
            'facts': self.facts,
        })

    def getGraph(self, path="../full_static/graph/fish.gv", view=False):
        graph = self.matcher.show_network()
        graph.format = 'svg'
        graph.render(path, view=False)

