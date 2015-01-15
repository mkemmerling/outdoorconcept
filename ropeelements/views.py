"""Rope element views."""
from django.shortcuts import render_to_response
from django.template import RequestContext

import django_filters
from rest_framework import filters
from rest_framework import generics

from . import models
from . import serializers


class KindListView(generics.ListAPIView):
    """API endpoint to list rope element kinds."""
    queryset = models.Kind.objects.all()
    serializer_class = serializers.KindSerializer


class ElementFilter(django_filters.FilterSet):
    """Rope element filter set."""

    kind = django_filters.NumberFilter(name="kind__id")

    class Meta:
        model = models.Element
        filter_fields = ('kind__id', 'child_friendly', 'accessible', 'canope')


class ElementListView(generics.ListAPIView):
    """API endpoint to list rope elements."""
    queryset = models.Element.objects.all()
    serializer_class = serializers.ElementSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ElementFilter


def ropeelements(request, **kwargs):
    """Rope elements template view."""
    contact = models.Config.objects.get(variable='contact')
    ssb_config = models.Config.objects.get(variable='ssb')
    powerfan_config = models.Config.objects.get(variable='powerfan')
    return render_to_response(
        'ropeelements.html', {
            'contact_url': contact.url,
            'ssb_url': ssb_config.url,
            'ssb_title': ssb_config.text,
            'powerfan_url': powerfan_config.url,
            'powerfan_title': powerfan_config.text,
        }, RequestContext(request))
