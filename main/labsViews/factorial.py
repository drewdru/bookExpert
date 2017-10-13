from django.shortcuts import render
from django.template import Context, RequestContext
from main.pyknowEngines import factorial

def factorialView(request):
    factorialEngine = factorial.ComputeFactorial()
    factorialEngine.reset()
    factorialEngine.run(10)
    factorialEngine.getGraph()
    return render(request, 'labs/factorial.html', {
        'facts': factorialEngine.facts,
        'network': factorialEngine.matcher.show_network().source,
    })
