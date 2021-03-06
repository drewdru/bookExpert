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
