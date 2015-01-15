"""Siebert form views."""
from django.shortcuts import render_to_response
from django.template import RequestContext


def siebert(request, **kwargs):
    """Siebert form template view."""
    return render_to_response(
        'siebert.html', {
        }, RequestContext(request))
