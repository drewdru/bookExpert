import pyknow

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

    def declareNewFacts(self, newFactKey, facts, request):
        newFact = request.POST.get(newFactKey, '')
        for indx, fact in enumerate(facts):
            facts[indx]['oldValue'] = request.POST.get(fact['key'], '')
            facts[indx]['newValue'] = request.POST.get(fact['fustyKey'], '')
        if newFact != '':
            newPostData = {}
            fustyPostData = []
            for indx, fact in enumerate(facts):
                newPostValue = self.updateParametr(fact['button'], 
                    fact['oldValue'], fact['newValue'], request)
                if fact['fustyKey'] == newFactKey:
                    newFact = newPostValue
                newPostData[facts[indx]['key']] = newPostValue
                fustyPostData.append(facts[indx]['fustyKey'])
                fustyPostData.append(facts[indx]['button'])
            request = self.changePostParametrs(request, newPostData, fustyPostData)
            if newFact != '':
                self.declareFeatures(newFact.split('&'))
            return True, request
        return False, request
