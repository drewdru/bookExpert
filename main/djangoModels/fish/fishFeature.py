from django.db import models
from django.contrib import admin

class FishFeature(models.Model):
    feature = models.CharField(max_length=30)

    def __str__(self):
        return str(self.feature)

    class Meta:
        ordering = ('feature',)

admin.site.register(FishFeature)