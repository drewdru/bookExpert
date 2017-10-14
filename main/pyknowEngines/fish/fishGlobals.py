from django.http import HttpRequest
global request
request = HttpRequest()
# class FishGlobals(object):
#     _instance = None
#     def __new__(FishGlobals, *args, **kwargs):
#         if not isinstance(FishGlobals._instance, FishGlobals):
#             FishGlobals._instance = object.__new__(FishGlobals, *args, **kwargs)
#         return FishGlobals._instance

#     # def __init__(self):
#     #     self.request = HttpRequest()
    
#     # def initRequest(self, request):
#     #     self.request = request
