
# from main.djangoModels.fish import fish
# from .factListConverter import listToStr

# import pyknow

# class FishFact(pyknow.Fact):
#     @classmethod
#     def from_django_model(cls, obj):
#         detachments = listToStr(obj.detachments.all())
#         features = listToStr(obj.features.all())
#         kinds = listToStr(obj.kinds.all())
#         return cls(fishName=obj.fishName,
#                    detachments=detachments,
#                    features=features,
#                    kinds=kinds)

#     @classmethod
#     def getFishFacts(cls):
#         factList = []
#         for fishObject in fish.Fish.objects.all():
#             factList.append(FishFact.from_django_model(fishObject))
#         return factList

#     def save_to_db(self):
#         return fish.Fish.objects.create(**self)