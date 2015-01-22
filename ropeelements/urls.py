"""Rope elements URL configuration."""
from functools import partial

from django.conf.urls import patterns
from django.conf.urls import url

from . import views

urlpatterns = patterns(
    '',
    url(r'^en/ng/ropeelements$', partial(views.ropeelements, language='en'),
        name='ropeelement_list_en'),
    url(r'^de/ng/ropeelements$', partial(views.ropeelements, language='de'),
        name='ropeelement_list_de'),
    url(r'^api/ropeelements$', views.ElementListView.as_view(),
        name='ropeelement-list'),
)
