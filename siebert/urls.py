"""Rope elements URL configuration."""
from django.conf.urls import patterns
from django.conf.urls import url

from . import views

urlpatterns = patterns(
    '',
    url(r'^ng/siebert$', views.siebert, name='siebert_form'),
)
