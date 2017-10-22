import pyknow
from main.pyknowEngines.fish import fishGlobals

class BaseEngine(pyknow.KnowledgeEngine):
    def getGraph(self, path="../full_static/graph/fish.gv", view=False):
        graph = self.matcher.show_network()
        graph.format = 'svg'
        graph.render(path, view=False)

    def changePostParametrs(self, request, postMap=None, postDelete=None):
        mutable = request.POST._mutable
        request.POST._mutable = True
        for key, value in postMap.items():
            request.POST[key] = value
        for key in postDelete:
            try:
                request.POST.pop(key)
            except KeyError:
                pass
        request.POST._mutable = mutable
        return request

    def updateParametr(self, buttonName, oldValue, newValue, request):
        if oldValue == '' and buttonName in request.POST:
            oldValue = newValue
        elif buttonName in request.POST:
            oldValue += '&{}'.format(newValue)
        return oldValue

    def getNewParams(self, objList):            
        newIdunnoFeatures = ''
        newIgnoreFeatures = ''
        for feature in objList:
            if newIdunnoFeatures == '':
                newIdunnoFeatures = '{}'.format(feature.id)
            else:
                newIdunnoFeatures += '&{}'.format(feature.id)
            if newIgnoreFeatures == '':
                newIgnoreFeatures = '{}'.format(feature.id)
            else:
                newIgnoreFeatures += '&{}'.format(feature.id)
        return newIdunnoFeatures, newIgnoreFeatures

    def splitFactsString(self, factsString):
        facts = []
        if factsString:
            facts = list(int(x) for x in factsString.split('&'))
        return facts

    def declareNewFacts(self):
        isUpdate = False
        for newFactKey, data in fishGlobals.newFacts.items():
            for indx, fact in enumerate(data['facts']):
                data['facts'][indx]['oldValue'] = fishGlobals.request.POST.get(fact['key'], '')
                data['facts'][indx]['newValue'] = fishGlobals.request.POST.get(fact['fustyKey'], '')
            newFact = fishGlobals.request.POST.get(newFactKey, '')
            if newFact != '':
                newPostData = {}
                fustyPostData = []
                for indx, fact in enumerate(data['facts']):
                    newPostValue = self.updateParametr(fact['button'], 
                        fact['oldValue'], fact['newValue'], fishGlobals.request)
                    if fact['fustyKey'] == newFactKey:
                        newFact = newPostValue
                    newPostData[data['facts'][indx]['key']] = newPostValue
                    fustyPostData.append(data['facts'][indx]['fustyKey'])
                    fustyPostData.append(data['facts'][indx]['button'])
                fishGlobals.request = self.changePostParametrs(fishGlobals.request, newPostData,
                        fustyPostData)
                if newFact != '':
                    getattr(self, data['method'])(newFact.split('&'))
                    isUpdate = True
        return isUpdate, fishGlobals.request
    
    def declareFeatures(self, features):
        from main.pyknowModels.fish.features import Features
        print("I'm a FEATURES: ", features)
        for feature in features:
            self.declare(Features(feature=feature))

    def declareKinds(self, kinds):
        from main.pyknowModels.fish.kinds import Kinds
        print("I'm a KINDS: ", kinds)
        for kind in kinds:
            self.declare(Kinds(kind=kind))

    def declareDetachments(self, detachments):
        print("I'm a DETACHMENTS: ", detachments)
        for detachment in detachments:
            self.declare(Detachments(detachment=detachment))

    # def declareNewFacts(self, newFactKey, facts, request):
    #     newFact = request.POST.get(newFactKey, '')
    #     for indx, fact in enumerate(facts):
    #         facts[indx]['oldValue'] = request.POST.get(fact['key'], '')
    #         facts[indx]['newValue'] = request.POST.get(fact['fustyKey'], '')
    #     if newFact != '':
    #         newPostData = {}
    #         fustyPostData = []
    #         for indx, fact in enumerate(facts):
    #             newPostValue = self.updateParametr(fact['button'], 
    #                 fact['oldValue'], fact['newValue'], request)
    #             if fact['fustyKey'] == newFactKey:
    #                 newFact = newPostValue
    #             newPostData[facts[indx]['key']] = newPostValue
    #             fustyPostData.append(facts[indx]['fustyKey'])
    #             fustyPostData.append(facts[indx]['button'])
    #         request = self.changePostParametrs(request, newPostData, fustyPostData)
    #         if newFact != '':
    #             self.declareFeatures(newFact.split('&'))
    #         return True, request
    #     return False, request

