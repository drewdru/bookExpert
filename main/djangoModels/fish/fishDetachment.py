from django.db import models
from django.contrib import admin
from main.djangoModels.fish.fishFeature import FishFeature
from main.djangoModels.fish.fishKind import FishKind

class FishDetachment(models.Model):
    detachment = models.CharField(max_length=30)
    features = models.ManyToManyField(FishFeature, null=True, blank=True, default=None)
    kinds = models.ManyToManyField(FishKind, null=True, blank=True, default=None)

    def __str__(self):
        return str(self.detachment)

    class Meta:
        ordering = ('detachment',)


admin.site.register(FishDetachment)
