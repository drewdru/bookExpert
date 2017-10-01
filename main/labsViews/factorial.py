from django.shortcuts import render
from django.template import Context, RequestContext
from main.pyknowModels import factorial

def factorialView(request):
    factorialEngine = factorial.ComputeFactorial()
    factorialEngine.reset()
    factorialEngine.declare(factorial.Factorial(1, 1))
    factorialEngine.run(10)
    factorialEngine.getGraph()
    return render(request, 'labs/factorial.html', {
        'facts': factorialEngine.facts,
        'network': factorialEngine.matcher.show_network().source,
    })
