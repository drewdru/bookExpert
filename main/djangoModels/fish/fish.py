from django.db import models
from django.contrib import admin
from main.djangoModels.fish.fishDetachment import FishDetachment
from main.djangoModels.fish.fishFeature import FishFeature
from main.djangoModels.fish.fishKind import FishKind

class Fish(models.Model):
    fishName = models.CharField(max_length=30)
    detachments = models.ManyToManyField(FishDetachment, null=True, blank=True)
    features = models.ManyToManyField(FishFeature, null=True, blank=True)
    kinds = models.ManyToManyField(FishKind, null=True, blank=True)

    def __str__(self):
        return self.fishName

    class Meta:
        ordering = ('fishName',)

admin.site.register(Fish)
