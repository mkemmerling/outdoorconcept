"""Rope element views."""
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import translation

from rest_framework import generics

from . import models
from . import serializers


class ElementListView(generics.ListAPIView):
    """API endpoint to list rope elements."""
    queryset = models.Element.objects.all()
    serializer_class = serializers.ElementSerializer

    def get(self, request, *args, **kwargs):
        translation.activate(request.path.split('/')[1])
        return self.list(request, *args, **kwargs)


def ropeelements(request, **kwargs):
    """Rope elements template view."""
    contact = models.Config.objects.get(variable='contact')
    ssb_config = models.Config.objects.get(variable='ssb')
    powerfan_config = models.Config.objects.get(variable='powerfan')

    translation.activate(request.path.split('/')[1])

    return render_to_response(
        'ropeelements.html', {
            'contact_url': contact.url,
            'ssb_url': ssb_config.url,
            'ssb_title': ssb_config.text,
            'powerfan_url': powerfan_config.url,
            'powerfan_title': powerfan_config.text,
        }, RequestContext(request))
