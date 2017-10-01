from django.conf.urls import url, include
from django.contrib import admin
from . import views
from .labsViews import factorial, fish, greetings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^factorial$', factorial.factorialView),
    url(r'^fish$', fish.fishView),
    url(r'^greetings$', greetings.greetingsView),
    url(r'^$', views.index),
]