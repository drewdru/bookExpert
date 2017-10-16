from django.db import models
from django.contrib import admin
from main.djangoModels.fish.fishFeature import FishFeature

class FishKind(models.Model):
    kind = models.CharField(max_length=30)
    features = models.ManyToManyField(FishFeature, null=True,
            blank=True, default=None)

    def __str__(self):
        return str(self.kind)

    class Meta:
        ordering = ('kind',)

admin.site.register(FishKind)
