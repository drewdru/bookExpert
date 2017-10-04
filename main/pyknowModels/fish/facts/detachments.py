
# from main.djangoModels.fish import fishDetachment
# from .factListConverter import listToStr
# import pyknow

# class Detachments(pyknow.Fact):
#     @classmethod
#     def from_django_model(cls, obj):
#         features = listToStr(obj.features.all())
#         kinds = listToStr(obj.kinds.all())
#         return cls(detachment=obj.detachment,
#                    features=features,
#                    kinds=kinds)

#     @classmethod
#     def getNotFishDetachments(cls):
#         detachmentList = []
#         for detachment in fishDetachment.FishDetachment.objects.all():
#             detachmentList.append(pyknow.NOT(
#                 Detachments.from_django_model(detachment)))
#         return detachmentList

#     def save_to_db(self):
#         return fishDetachment.FishDetachment.objects.create(**self)