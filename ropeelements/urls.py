"""Rope elements URL configuration."""
from django.conf.urls import patterns
from django.conf.urls import url

from . import views

urlpatterns = patterns(
    '',
    url(r'^ng/ropeelements$', views.ropeelements,
        name='ropeelement_list'),
    url(r'^api/ropeelements$', views.ElementListView.as_view(),
        name='ropeelement-list'),
)
